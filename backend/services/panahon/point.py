import os
import threading
import requests

TOKEN = os.environ.get("PANAHON_API_TOKEN")

POINT_CACHE = {}
CACHE_LOCK = threading.Lock()

def fetch_point_rainfall(
    lat,
    lon,
    forecast_time,
    init_time,
):

    key = (
        round(lat, 6),
        round(lon, 6),
        forecast_time,
        init_time,
    )

    with CACHE_LOCK:
        if key in POINT_CACHE:
            return POINT_CACHE[key]

    url = (
        "https://www.panahon.gov.ph/api/v1/tiles/point"
        f"?url=prate_accum"
        f"&lat={lat}"
        f"&lon={lon}"
        f"&t={forecast_time}"
        f"&init={init_time}"
        f"&token={TOKEN}"
    )

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    rainfall = r.json().get("values", [0])[0] or 0

    with CACHE_LOCK:
        POINT_CACHE[key] = rainfall

    return rainfall