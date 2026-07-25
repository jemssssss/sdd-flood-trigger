from pathlib import Path
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from django.conf import settings
from services.ecmwf.datetime import (build_ecmwf_request)
from services.ecmwf.sampler import (load_rainfall_dataset)
from services.sentinel.passes import (get_sentinel_pass_info)

ROOT = settings.BASE_DIR.parent

def compute_ecmwf_footprints(
    forecast_time,
    init_time,
):

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

    footprints = gpd.read_file(footprint_file)
    
    footprints = footprints.set_crs(
        "EPSG:4326",
        allow_override=True,
    )

    strips = pass_info["strips"]
    footprints = footprints[
        footprints["TileNumber"]
        .str[0]
        .isin(strips)
    ].copy()

    if footprints.empty:

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

    request = build_ecmwf_request(
        init_time,
        forecast_time,
    )

    sampler = load_rainfall_dataset(
        request["date"],
        request["time"],
        request["step"],
    )

    coords = sampler["coords"]
    rainfall = sampler["rainfall"]
    tree = sampler["tree"]

    summary = {
        "moderate": [],
        "heavy": [],
    }

    for _, row in footprints.iterrows():
        polygon = row.geometry
        minx, miny, maxx, maxy = polygon.bounds

        mask = (
            (coords[:, 0] >= minx)
            & (coords[:, 0] <= maxx)
            & (coords[:, 1] >= miny)
            & (coords[:, 1] <= maxy)
        )

        indices = np.where(mask)[0]
        values = []
        for idx in indices:
            pt = Point(coords[idx])
            if polygon.covers(pt):
                values.append(float(rainfall[idx]))

        if not values:
            centroid = polygon.centroid
            _, nearest = tree.query(
                [
                    centroid.x,
                    centroid.y,
                ]
            )

            values.append(float(rainfall[nearest]))

        average = float(np.mean(values))

        row["ecmwfRainfall"] = average
        if 60 <= average <= 180:

            summary["moderate"].append(
                row["TileNumber"]
            )

        elif average > 180:
            summary["heavy"].append(
                row["TileNumber"]
            )

        footprints.loc[
            row.name,
            "ecmwfRainfall",
        ] = average

    summary["moderate"].sort()
    summary["heavy"].sort()

    return {
        "geojson": footprints.__geo_interface__,
        "summary": summary,
        "passInfo": pass_info,
    }