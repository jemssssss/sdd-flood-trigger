from pathlib import Path
import geopandas as gpd
import numpy as np
from django.conf import settings
from shapely.geometry import Point
from services.gpm.datetime import (build_gpm_request)
from services.gpm.sampler import (load_rainfall_dataset)
from services.sentinel.passes import (get_sentinel_pass_info)

ROOT = settings.BASE_DIR.parent

def compute_gpm_footprints(
    forecast_time
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

    end_time = build_gpm_request(forecast_time)
    sampler = load_rainfall_dataset(end_time)
    rain = sampler["rain"]
    latitudes = sampler["latitudes"]
    longitudes = sampler["longitudes"]
    coords = sampler["coords"]
    tree = sampler["tree"]

    rain_values = rain.values

    summary = {
        "moderate": [],
        "heavy": [],
    }

    for _, row in footprints.iterrows():

        polygon = row.geometry

        minx, miny, maxx, maxy = polygon.bounds

        lon_idx = np.where(
            (longitudes >= minx)
            & (longitudes <= maxx)
        )[0]

        lat_idx = np.where(
            (latitudes >= miny)
            & (latitudes <= maxy)
        )[0]

        values = []

        if len(lon_idx) and len(lat_idx):

            subset_lon = longitudes[lon_idx]
            subset_lat = latitudes[lat_idx]

            xx, yy = np.meshgrid(
                subset_lon,
                subset_lat,
                indexing="xy",
            )

            from shapely import points, covers

            pts = points(
                xx.ravel(),
                yy.ravel(),
            )

            inside = covers(
                polygon,
                pts,
            )

            subset = rain_values[
                np.ix_(lon_idx, lat_idx)
            ].T

            values = subset.ravel()[inside]

            values = values[
                ~np.isnan(values)
            ]

        #
        # Fallback to nearest grid point
        #

        if len(values) == 0:

            centroid = polygon.centroid

            _, nearest = tree.query(
                [centroid.x, centroid.y],
                k=4,
            )

            nearest_values = rain_values.ravel()[nearest]

            nearest_values = nearest_values[
                ~np.isnan(nearest_values)
            ]

            values = nearest_values

        average = float(np.mean(values))

        footprints.loc[
            row.name,
            "gpmRainfall",
        ] = average

        if 60 <= average <= 180:

            summary["moderate"].append(
                row["TileNumber"]
            )

        elif average > 180:

            summary["heavy"].append(
                row["TileNumber"]
            )

    summary["moderate"].sort()
    summary["heavy"].sort()

    return {
        "geojson": footprints.__geo_interface__,
        "summary": summary,
        "passInfo": pass_info,
    }