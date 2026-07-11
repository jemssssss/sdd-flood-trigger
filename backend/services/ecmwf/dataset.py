import earthkit.data as ek

ek.config.set({
    "cache-policy": "user",
    "user-cache-directory": "./earthkit_cache",
})


def load_dataset(
    date,
    time,
    step,
):
    """
    Downloads (or retrieves from cache)
    one ECMWF Open Data forecast.
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

    return ds.to_xarray()