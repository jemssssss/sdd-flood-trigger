from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil

import earthaccess
from dotenv import load_dotenv
from django.conf import settings

# ============================================================
# SETTINGS
# ============================================================

DOWNLOAD_DIR = (
    settings.BASE_DIR
    / "data"
    / "gpm_cache"
)

DOWNLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

SHORT_NAME = "GPM_3IMERGHHE"

_logged_in = False


# ============================================================
# LOGIN
# ============================================================

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

    print(
        "Earthdata login successful."
    )


# ============================================================
# CACHE DIRECTORY
# ============================================================

def get_cache_directory(
    forecast_time_utc: datetime,
):

    folder = (
        DOWNLOAD_DIR
        / forecast_time_utc.strftime(
            "%Y%m%d_%H%M"
        )
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return folder


# ============================================================
# CLEAN OLD CACHE
# ============================================================

def cleanup_cache(
    active_folder: Path,
):

    for folder in DOWNLOAD_DIR.iterdir():

        if (
            folder.is_dir()
            and folder != active_folder
        ):

            print(
                f"Deleting old cache: {folder.name}"
            )

            shutil.rmtree(
                folder,
                ignore_errors=True,
            )


# ============================================================
# SEARCH IMERG HALF-HOURLY
# ============================================================

def search_granules(
    init_time_utc: datetime,
    forecast_time_utc: datetime,
):

    granules = earthaccess.search_data(

        short_name=SHORT_NAME,

        temporal=(

            init_time_utc.isoformat(),
            forecast_time_utc.isoformat(),

        ),

    )

    if not granules:

        raise RuntimeError(
            "No IMERG half-hourly granules found."
        )

    return granules


# ============================================================
# DOWNLOAD
# ============================================================

def download_imerg_24h(
    forecast_time_utc: datetime,
):

    login()

    
    available_until = (datetime.now(timezone.utc) - timedelta(hours=5)) # IMERG Early normally lags by ~5 hours.

    if forecast_time_utc > available_until:
        raise RuntimeError(
            "Requested forecast time "
            "is newer than available "
            "IMERG Early data."
        )

    init_time_utc = (
        forecast_time_utc
        - timedelta(days=1)
    )

    cache_folder = get_cache_directory(forecast_time_utc)
    cleanup_cache(cache_folder)

    granules = search_granules(
        init_time_utc,
        forecast_time_utc,
    )

    # Reuse cached files whenever possible.
    cached = sorted(cache_folder.glob("*.HDF5"))

    if len(cached) == len(granules):
        print(
            f"Using cached observation "
            f"({len(cached)} files)."
        )
        return cached

    print()
    print(
        f"Downloading "
        f"{len(granules)} "
        f"IMERG granules..."
    )

    downloaded = earthaccess.download(
        granules,
        local_path=cache_folder,

    )

    downloaded = sorted(
        Path(file)
        for file in downloaded
    )

    print()

    print(
        f"Downloaded "
        f"{len(downloaded)} files."
    )

    return downloaded