from datetime import datetime, timedelta, timezone

# ------------
# CONSTANTS
# ------------

# Dashboard times are Philippine Standard Time.
PST_OFFSET = timedelta(hours=8)

# IMERG Early is typically available
# about 5 hours behind real time.
IMERG_EARLY_LATENCY = timedelta(hours=5)

# ---------------------
# PARSE DASHBOARD TIME
# ---------------------

def parse_forecast_time(
    forecast_time: str,
) -> datetime:
    """
    Converts the dashboard ISO string into
    a timezone-aware Philippine datetime.

    Example input:
        2026-07-28T06:00:00
    """

    dt = datetime.fromisoformat(
        forecast_time.replace(
            "Z",
            "",
        )
    )

    return dt.replace(
        tzinfo=timezone(PST_OFFSET)
    )

def build_gpm_request(
    forecast_time: str,
):

    forecast_pst = parse_forecast_time(forecast_time)

    forecast_utc = forecast_pst.astimezone(timezone.utc)
    init_utc = (forecast_utc - timedelta(days=1))

    return (
        forecast_utc,
        init_utc,
    )


# --------------------
# DATA AVAILABILITY
# --------------------

def latest_available_time():
    """
    Returns the newest UTC timestamp that
    should be available from IMERG Early.
    """

    return (
        datetime.now(timezone.utc)
        - IMERG_EARLY_LATENCY
    )


def validate_request_time(
    forecast_time_utc: datetime,
):

    latest = latest_available_time()
    if forecast_time_utc > latest:

        raise RuntimeError(

            "Requested forecast time "
            "is newer than the latest "
            "available IMERG Early data."

        )