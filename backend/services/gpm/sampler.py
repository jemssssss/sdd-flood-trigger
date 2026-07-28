import numpy as np
import xarray as xr
from scipy.spatial import cKDTree
from services.gpm.dataset import (download_imerg_24h)
from services.gpm.datetime import (build_gpm_request, validate_request_time)

def build_24h_accumulation(
    files,
):
    """
    Builds a 24-hour rainfall accumulation
    from IMERG Early Half-Hourly granules.

    IMERG precipitation is in mm/hr.

    Therefore each file contributes

        precipitation × 0.5 hr

    to the accumulation.
    """

    accumulation = None

    for file in files:

        ds = xr.open_dataset(
            file,
            engine="netcdf4",
            group="Grid",
        )

        rain = ds["precipitation"].isel(
            time=0,
        )

        # Convert half-hour rainfall rate
        # into accumulated rainfall.        

        rain_mm = rain * 0.5

        if accumulation is None:
            accumulation = rain_mm
        else:
            accumulation += rain_mm

        ds.close()

    return accumulation

def load_rainfall_dataset(
    forecast_time,
):
    """
    Returns a dictionary containing

        accumulated rainfall
        latitude array
        longitude array
        KD-tree

    ready for polygon sampling.
    """

    forecast_utc, _ = build_gpm_request(forecast_time)
    validate_request_time(forecast_utc)
    files = download_imerg_24h(forecast_utc)
    rain = build_24h_accumulation(files)

    latitudes = rain["lat"].values
    longitudes = rain["lon"].values

    lon_grid, lat_grid = np.meshgrid(
        longitudes,
        latitudes,
        indexing="xy"
    )

    coords = np.column_stack(
        (
            lon_grid.ravel(),
            lat_grid.ravel(),
        )
    )

    tree = cKDTree(coords)

    return {

        "rain": rain,

        "latitudes": latitudes,
        "longitudes": longitudes,

        "coords": coords,
        "tree": tree,

    }