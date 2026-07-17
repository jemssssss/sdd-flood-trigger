from datetime import date, datetime
from typing import Any, Union

NO_SATELLITE_PASS = "No Satellite Pass"
DEFAULT_SATELLITE = "Sentinel-1A"

# Future additional satellites can be registered here
SATELLITES: dict[str, dict[str, Any]] = {
    "Sentinel-1A": {
        "aliases": {"S1A", "SENTINEL-1A"},
        "footprintFile": "s1a_footprints.geojson",
        "repeatDays": 12,
        "stripReferences": {
            "A": date(2026, 1, 31),
            "B": date(2026, 1, 26),
            "C": date(2026, 1, 21),
            "D": date(2026, 1, 28),
            "E": date(2026, 1, 23),
        },
    },
}

DateInput = Union[date, datetime, str]

def get_satellite_config(satellite: str) -> dict[str, Any]:
    satellite_key = satellite.strip().upper().replace("_", "-")

    for name, config in SATELLITES.items():
        if satellite_key in config["aliases"]:
            return {"name": name, **config}

    available = ", ".join(SATELLITES)
    raise ValueError(
        f"Unsupported satellite: {satellite}. Available satellites: {available}."
    )


def get_sentinel_pass_info(satellite: str, pass_date: DateInput) -> dict[str, Any]:
    config = get_satellite_config(satellite)
    target_date = _to_date(pass_date)
    strip = get_sentinel_pass(config["name"], target_date)

    return {
        "satellite": config["name"],
        "passDate": target_date.isoformat(),
        "hasPass": strip != NO_SATELLITE_PASS,
        "strip": None if strip == NO_SATELLITE_PASS else strip,
    }


def get_sentinel_pass(satellite: str, pass_date: DateInput) -> str:
    # Return the Philippines strip for a satellite pass, or no-pass text.
    config = get_satellite_config(satellite)
    target_date = _to_date(pass_date)

    for strip, reference_date in config["stripReferences"].items():
        elapsed_days = (target_date - reference_date).days
        if elapsed_days % config["repeatDays"] == 0:
            return strip

    return NO_SATELLITE_PASS


def _to_date(value: DateInput) -> date:
    # Normalize supported input forms without applying a timezone conversion.
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError as exc:
            raise ValueError("pass_date must be an ISO-8601 date or datetime.") from exc
    raise TypeError("pass_date must be a date, datetime, or ISO-8601 string.")
