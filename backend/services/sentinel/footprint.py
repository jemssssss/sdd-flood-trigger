import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from services.sentinel.point import fetch_point_rainfall


ROOT = settings.BASE_DIR.parent

FOOTPRINT_FILE = (
    ROOT
    / "web"
    / "public"
    / "data"
    / "s1a_footprints.geojson"
)

SAMPLE_FILE = (
    ROOT
    / "web"
    / "public"
    / "data"
    / "footprintSamplePoints.json"
)


def compute_footprints(forecast_time, init_time):

    # Load footprint polygons
    with open(FOOTPRINT_FILE, encoding="utf-8") as f:
        geojson = json.load(f)

    # Load sample points
    with open(SAMPLE_FILE, encoding="utf-8") as f:
        sample_points = json.load(f)

    # Convert list into dictionary for O(1) lookup
    sample_lookup = {
        item["tile"]: item["samplePoints"]
        for item in sample_points
    }

    summary = {
        "moderate": [],
        "heavy": [],
    }

    def process_feature(feature):

        tile = feature["properties"]["TileNumber"]

        samples = sample_lookup.get(tile)

        if samples is None:
            feature["properties"]["averageRainfall"] = None
            return feature, None

        # Fetch every point simultaneously
        with ThreadPoolExecutor(max_workers=15) as executor:

            rainfall_values = list(
                executor.map(
                    lambda point: fetch_point_rainfall(
                        point["lat"],
                        point["lon"],
                        forecast_time,
                        init_time,
                    ),
                    samples,
                )
            )

        average = (
            sum(rainfall_values)
            / len(rainfall_values)
        )

        feature["properties"]["averageRainfall"] = average

        category = None

        if 60 <= average <= 180:
            category = ("moderate", tile)

        elif average > 180:
            category = ("heavy", tile)

        return feature, category

    # Process all footprints simultaneously
    with ThreadPoolExecutor(max_workers=8) as executor:

        results = list(
            executor.map(
                process_feature,
                geojson["features"],
            )
        )

    processed_features = []

    for feature, category in results:

        processed_features.append(feature)

        if category is not None:
            level, tile = category
            summary[level].append(tile)

    summary["moderate"].sort()
    summary["heavy"].sort()

    geojson["features"] = processed_features

    return {
        "geojson": geojson,
        "summary": summary,
    }