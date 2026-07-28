from pathlib import Path
import geopandas as gpd
import numpy as np
from django.conf import settings
from shapely import covers, points
from services.gpm.sampler import load_rainfall_dataset
from services.sentinel.passes import get_sentinel_pass_info

ROOT = settings.BASE_DIR.parent

def compute_gpm_footprints(
    forecast_time,
):

    pass_info = get_sentinel_pass_info(
        forecast_time,
    )

    # No satellite pass.
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

    # ------------------------
    # Load footprint GeoJSON
    # ------------------------

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

    # Keep only strips that actually passed.

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

    # ----------------------------
    # Load accumulated rainfall
    # ----------------------------

    sampler = load_rainfall_dataset(forecast_time)
    rain = sampler["rain"]
    latitudes = sampler["latitudes"]
    longitudes = sampler["longitudes"]

    tree = sampler["tree"]
    rain_values = rain.values

    summary = {
        "moderate": [],
        "heavy": []
    }

    # ------------------------
    # Sample every footprint
    # ------------------------

    for index, row in footprints.iterrows():
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
        values = np.array([])

        # Normal polygon sampling.
        if len(lon_idx) > 0 and len(lat_idx) > 0:
            subset_lon = longitudes[lon_idx]
            subset_lat = latitudes[lat_idx]
            xx, yy = np.meshgrid(
                subset_lon,
                subset_lat,
                indexing="xy"
            )
            pts = points(
                xx.ravel(),
                yy.ravel()
            )
            inside = covers(
                polygon,
                pts
            )
            subset = rain_values[np.ix_(lon_idx, lat_idx)].T
            values = subset.ravel()[inside]
            values = values[~np.isnan(values)]
        
        # Fallback:
        # use four nearest pixels.
        method = "inside_polygon"
        if values.size == 0:
            centroid = polygon.centroid
            _, nearest = tree.query(
                [
                    centroid.x,
                    centroid.y,
                ],
                k=4
            )

            values = rain_values.ravel()[nearest]
            values = values[~np.isnan(values)]

            method = "nearest_4"

        # No usable rainfall.
        if values.size == 0:
            average = np.nan
            method = "no_data"
        else:
            average = float(values.mean())

        footprints.loc[
            index,
            "gpmRainfall",
        ] = average

        footprints.loc[
            index,
            "samplingMethod",
        ] = method

        # Flood summary.
        if np.isnan(average):
            continue

        tile = row["TileNumber"]

        if 60 <= average <= 180:
            summary["moderate"].append(tile)

        elif average > 180:
            summary["heavy"].append(tile)

    summary["moderate"].sort()
    summary["heavy"].sort()

    return {

        "geojson": footprints.__geo_interface__,
        "summary": summary,
        "passInfo": pass_info,

    }