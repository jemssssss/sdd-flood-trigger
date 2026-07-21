import numpy as np
import xarray as xr
from scipy.spatial import cKDTree

from services.gpm.dataset import (
    login,
    download_imerg,
)


def load_rainfall_dataset(end_time):
    """
    Downloads (or reuses) the latest IMERG Daily file,
    opens it with xarray,
    and prepares everything needed for polygon sampling.
    """

    login()

    local_file = download_imerg(end_time)

    ds = xr.open_dataset(local_file)

    rain = ds["precipitation"].isel(time=0)

    rainfall = rain.values

    latitudes = rain["lat"].values
    longitudes = rain["lon"].values

    lon_grid, lat_grid = np.meshgrid(
        longitudes,
        latitudes,
        indexing="xy",
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
        "tree": tree,
        "coords": coords,
    }