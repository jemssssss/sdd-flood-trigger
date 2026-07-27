from datetime import date, datetime, timedelta
from typing import Any, Union

NO_SATELLITE_PASS = "No Satellite Pass"

DateInput = Union[date, datetime, str]

# ------------
# Satellites
# ------------

SATELLITES: dict[str, dict[str, Any]] = {
    "Sentinel-1A": {
        "aliases": {"S1A", "SENTINEL-1A"},
        "footprintFile": "s1a_footprints.geojson",
        "footprintFilePoints": "footprintSamplePoints.json",
        "repeatDays": 12,
        "priority": 1,
        "stripReferences": {
            "A": datetime(2026, 1, 31, 0, 0),
            "B": datetime(2026, 1, 26, 0, 0),
            "C": datetime(2026, 1, 21, 0, 0),
            "D": datetime(2026, 1, 28, 0, 0),
            "E": datetime(2026, 1, 23, 0, 0),
        },
    },

    "Sentinel-1C": {
        "aliases": {"S1C", "SENTINEL-1C"},
        "footprintFile": "s1c_footprints.geojson",
        "footprintFilePoints": "footprintSamplePoints_C.json",
        "repeatDays": 12,
        "priority": 2,
        "stripReferences": {
            "A": datetime(2026, 1, 1, 6),
            "B": datetime(2026, 1, 8, 6),
            "C": datetime(2026, 1, 3, 6),
            "D": datetime(2026, 1, 10, 6),
            "E": datetime(2026, 1, 5, 6),

            "X": datetime(2026, 1, 3, 18),
            "Y": datetime(2026, 1, 10, 18),
            "Z": datetime(2026, 1, 5, 18),
        },
    },
}

DEFAULT_SATELLITE = "Sentinel-1A" # long live da og

def _to_datetime(value: DateInput) -> datetime:

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(
            value,
            datetime.min.time(),
        )

    if isinstance(value, str):
        try:
            return datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise ValueError(
                "Invalid ISO datetime."
            ) from exc

    raise TypeError(
        "Expected date, datetime or ISO string."
    )


def get_satellite_config(
    satellite: str,
):

    key = satellite.upper().replace("_", "-")

    for name, config in SATELLITES.items():

        if (
            key == name.upper()
            or key in config["aliases"]
        ):
            return {
                "name": name,
                **config,
            }

    raise ValueError(
        f"Unsupported satellite: {satellite}"
    )


# ---------------
# Compute strips
# ---------------

def get_sentinel_passes(
    satellite: str,
    pass_time: DateInput,
):

    config = get_satellite_config(satellite)
    target = _to_datetime(pass_time)

    # Determine which orbit (hour) is active.
    pass_hours = sorted(
        {
            ref.hour
            for ref in config["stripReferences"].values()
        }
    )

    active_hour = None

    for hour in pass_hours:
        if target.hour >= hour:
            active_hour = hour

    if active_hour is None:
        return []

    strips = []

    for strip, reference in config["stripReferences"].items():
        # Ignore strips belonging to a different orbit.
        if reference.hour != active_hour:
            continue

        if target < reference:
            continue

        elapsed = target - reference

        if elapsed.days % config["repeatDays"] != 0:
            continue

        strips.append(strip)

    strips.sort()

    return strips

def get_active_satellite(
    pass_time: DateInput,
):

    target = _to_datetime(
        pass_time,
    )

    candidates = []

    for satellite in SATELLITES:

        strips = get_sentinel_passes(satellite, target)

        if not strips:
            continue

        config = get_satellite_config(satellite)
        candidates.append({
            "satellite": satellite,
            "priority": config["priority"],
            "footprintFile": config["footprintFile"],
            "footprintFilePoints": config["footprintFilePoints"],
            "strips": strips,
        })

    if not candidates:
        return None

    candidates.sort(
        key=lambda x: x["priority"],
        reverse=True,
    )

    return candidates[0]

def get_sentinel_pass_info(
    pass_time: DateInput,
):

    target = _to_datetime(pass_time)
    active = get_active_satellite(target)

    if active is None:

        return {

            "hasPass": False,
            "satellite": None,
            "footprintFile": None,
            "footprintFilePoints": None,
            "strips": [],
            "passDate": target.isoformat(),

        }

    return {

        "hasPass": True,
        "satellite": active["satellite"],
        "footprintFile": active["footprintFile"],
        "footprintFilePoints": active["footprintFilePoints"],
        "strips": active["strips"],
        "passDate": target.isoformat(),

    }

# -----------------------------------------
# Forecast and Initialization Timestamps
# -----------------------------------------

def get_active_accumulation_window(now=None):

    if now is None:
        now = datetime.now()

    today = now.replace(
        minute=0,
        second=0,
        microsecond=0,
    )    

    morning = today.replace(hour=6)
    evening = today.replace(hour=18)

    # Does today have a 6 PM pass?
    evening_pass = False
    for satellite in SATELLITES:
        strips = get_sentinel_passes(
            satellite,
            evening,
        )

        if any(
            strip in ("X", "Y", "Z") # X/Y/Z are evening strips
            for strip in strips
        ):
            evening_pass = True
            break

    if evening_pass and now >= evening:
        forecast = evening
    else:
        forecast = morning

        # before 6AM -> yesterday 6AM
        if now < morning:
            forecast -= timedelta(days=1)

    init = forecast - timedelta(days=1)
    
    print("Forecast Datetime:", forecast)
    print("Initial Datetime:", init)
    return {

        "forecast": forecast,
        "init": init,
        "hour": forecast.hour,

    }