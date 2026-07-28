import asyncio
import json
from pathlib import Path
import httpx
import statistics
from django.conf import settings
from services.sentinel.passes import (get_sentinel_pass_info)

ROOT = settings.BASE_DIR.parent
TOKEN = settings.PANAHON_API_TOKEN
POINT_URL = "https://www.panahon.gov.ph/api/v1/tiles/point"

# Maximum simultaneous requests
MAX_CONCURRENT_REQUESTS = 20

async def fetch_point(
    client,
    semaphore,
    lat,
    lon,
    forecast_time,
    init_time,
):

    params = {
        "url": "prate_accum",
        "lat": lat,
        "lon": lon,
        "t": forecast_time,
        "init": init_time,
        "token": TOKEN,
    }

    async with semaphore:

        try:
            response = await client.get(
                POINT_URL,
                params=params,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            rainfall = data.get("values", [0])[0]

            key = (
                round(lat, 8),
                round(lon, 8),
            )

            return key, float(rainfall or 0)
        except Exception as e:
            print(
                f"FAILED ({lat}, {lon}) -> {e}"
            )
            return (lat, lon), 0.0


async def compute_worker(
    forecast_time,
    init_time
):

    # -----------------------
    # Read files
    # -----------------------

    pass_info = get_sentinel_pass_info(forecast_time)

    if not pass_info["hasPass"]:
        return {
            "geojson": {
                "type": "FeatureCollection",
                "features": [],
            },
            "summary": {
                "moderate": [],
                "heavy": [],
            },
            "passInfo": pass_info,
        }

    footprint_file = (
        ROOT
        / "web"
        / "public"
        / "data"
        / pass_info["footprintFile"]
    )

    SAMPLE_FILE = (
            ROOT
            / "web"
            / "public"
            / "data"
            / pass_info["footprintFilePoints"]
        )

    with open(
        footprint_file,
        encoding="utf-8",
    ) as f:

        geojson = json.load(f)

    strips = set(pass_info["strips"])
    geojson["features"] = [
        feature
        for feature in geojson["features"]
        if (
            feature["properties"]
            .get("TileNumber", "")[:1]
            in strips
        )
    ]

    if not strips:
        return {
            "geojson": geojson,
            "summary": {"moderate": [], "heavy": []},
            "passInfo": pass_info,
        }

    with open(
        SAMPLE_FILE,
        encoding="utf-8",
    ) as f:

        sample_points = json.load(f)

    active_tiles = {
        feature["properties"]["TileNumber"]
        for feature in geojson["features"]
    }

    sample_lookup = {
        item["tile"]: item["samplePoints"]
        for item in sample_points
        if item["tile"] in active_tiles
    }

    # -----------------------
    # Build unique coordinate list
    # -----------------------

    unique_points = {}

    for samples in sample_lookup.values():

        for point in samples:

            key = (
                round(point["lat"], 8),
                round(point["lon"], 8),
            )

            unique_points[key] = point

    print(f"Unique sampling points: {len(unique_points)}")

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    limits = httpx.Limits(
        max_connections=MAX_CONCURRENT_REQUESTS,
        max_keepalive_connections=MAX_CONCURRENT_REQUESTS,
    )

    rainfall_cache = {}

    async with httpx.AsyncClient(
        limits=limits
    ) as client:

        tasks = [

            fetch_point(
                client,
                semaphore,
                point["lat"],
                point["lon"],
                forecast_time,
                init_time,
            )

            for point in unique_points.values()

        ]

        results = await asyncio.gather(*tasks)

    for key, rainfall in results:

        rainfall_cache[key] = rainfall

    # -----------------------
    # Compute averages
    # -----------------------

    summary = {
        "moderate": [],
        "heavy": [],
    }

    for feature in geojson["features"]:

        tile = feature["properties"]["TileNumber"]

        samples = sample_lookup.get(tile)

        if samples is None:

            feature["properties"]["averageRainfall"] = None

            continue

        rainfall = []

        for point in samples:

            key = (
                round(point["lat"], 8),
                round(point["lon"], 8),
            )

            rainfall.append(
                rainfall_cache[key]
            )
        # print(rainfall)
        average = (
            # sum(rainfall)
            # / len(rainfall)
            # or
            statistics.mean(rainfall)
            # or
            # max(rainfall)
        )

        feature["properties"]["averageRainfall"] = average

        if 60 <= average <= 180:

            summary["moderate"].append(tile)

        elif average > 180:

            summary["heavy"].append(tile)

    summary["moderate"].sort()
    summary["heavy"].sort()

    return {
        "geojson": geojson,
        "summary": summary,
        "passInfo": pass_info,
    }


def compute_footprints(
    forecast_time,
    init_time,
):

    return asyncio.run(
        compute_worker(
            forecast_time,
            init_time,
        )
    )
