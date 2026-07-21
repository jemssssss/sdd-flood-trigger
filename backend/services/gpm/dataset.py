import earthaccess
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
from django.conf import settings

DOWNLOAD_DIR = settings.BASE_DIR / "data" / "gpm_cache"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

_logged_in = False


def login():

    global _logged_in

    if _logged_in:
        return

    load_dotenv()

    earthaccess.login(
        strategy="environment",
        persist=False,
    )

    _logged_in = True
    print("Earthdata login successful.")

def download_imerg(end_time):

    start_time = end_time - timedelta(days=1)

    results = earthaccess.search_data(
        short_name="GPM_3IMERGDE",
        temporal=(
            start_time.isoformat(),
            end_time.isoformat(),
        ),
    )

    if not results:
        raise RuntimeError("No IMERG data found.")

    granule = results[0]

    return earthaccess.download(
        [granule],
        local_path=DOWNLOAD_DIR,
    )[0]