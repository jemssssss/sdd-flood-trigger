from datetime import datetime, timezone

def build_ecmwf_request(init_time, forecast_time):
    """
    Converts the frontend timestamps into the
    ECMWF Open Data request fields.

    Input
    -----
    init_time:
        2026-07-08T10:00:00Z

    forecast_time:
        2026-07-09T10:00:00

    Output
    ------
    {
        "date": "20260708",
        "time": "0000",
        "step": 24
    }
    """

    init_dt = datetime.fromisoformat(
        init_time.replace("Z", "+00:00")
    )

    fc_dt = datetime.fromisoformat(
        forecast_time
    )

    if fc_dt.tzinfo is None:
        fc_dt = fc_dt.replace(
            tzinfo=timezone.utc
        )

    step = int(
        (fc_dt - init_dt).total_seconds() / 3600
    )

    return {
        "date": init_dt.strftime("%Y%m%d"),
        "time": init_dt.strftime("%H%M"),
        "step": step,
    }