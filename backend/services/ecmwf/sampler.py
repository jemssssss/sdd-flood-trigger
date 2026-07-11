import numpy as np
import earthkit.data as ek
from scipy.spatial import cKDTree

# ---------------------------------------------------
# Earthkit cache
# ---------------------------------------------------

ek.config.set(
    {
        "cache-policy": "user",
        "user-cache-directory": "./earthkit_cache",
    }
)


def load_rainfall_dataset(
    date,
    time,
    step,
):
    """
    Download ECMWF Open Data
    and prepare everything needed
    for polygon sampling.
    """

    ds = ek.from_source(
        "ecmwf-open-data",
        request={
            "type": "fc",
            "stream": "oper",
            "levtype": "sfc",
            "param": "tp",
            "date": date,
            "time": time,
            "step": step,
        },
    )

    xr_ds = ds.to_xarray()

    tp = xr_ds.tp.values * 1000.0

    latitudes = xr_ds.latitude.values
    longitudes = xr_ds.longitude.values

    lon_grid, lat_grid = np.meshgrid(
        longitudes,
        latitudes,
    )

    coords = np.column_stack(
        (
            lon_grid.ravel(),
            lat_grid.ravel(),
        )
    )

    rainfall = tp.ravel()

    tree = cKDTree(coords)

    return {
        "coords": coords,
        "rainfall": rainfall,
        "tree": tree,
    }