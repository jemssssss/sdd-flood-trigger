from datetime import datetime, timedelta

def build_gpm_request(forecast_time):

    end = (
        datetime.fromisoformat(forecast_time)
        - timedelta(hours=6)
    )

    return end