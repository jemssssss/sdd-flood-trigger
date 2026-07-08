import os
import requests

TOKEN = os.environ.get("PANAHON_API_TOKEN")

def fetch_synoptic():

    url = (
        "https://www.panahon.gov.ph/api/v1/synop"
        f"?token={TOKEN}"
        "&parameter=rain"
    )

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    return r.json()


def fetch_aws():

    url = (
        "https://www.panahon.gov.ph/api/v1/aws"
        f"?token={TOKEN}"
        "&parameter=accumulated_rain_1h"
    )

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    return r.json()