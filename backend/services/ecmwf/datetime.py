from datetime import datetime, timezone, timedelta

def build_ecmwf_request(init_time, forecast_time):
    """
    Converts frontend PHT timestamps into an ECMWF Open Data request.
    Shifts 6 AM PHT targets to 2 AM PHT (18:00 UTC previous day)
    and computes the step.
    """
    
    # 1. Parse input timestamps (assumed to be PHT string like '2026-07-08T06:00:00')
    clean_init = init_time.replace("Z", "")
    clean_fc = forecast_time.replace("Z", "")
    
    init_dt_pht = datetime.fromisoformat(clean_init)
    fc_dt_pht = datetime.fromisoformat(clean_fc)

    # 2. Shift 6:00 AM local time target back by 4 hours to get 2:00 AM local time target
    init_target_pht = init_dt_pht - timedelta(hours=4)
    fc_target_pht = fc_dt_pht - timedelta(hours=4)

    # 3. Convert PHT (UTC+8) to UTC
    pht_offset = timedelta(hours=8)
    init_target_utc = init_target_pht - pht_offset
    fc_target_utc = fc_target_pht - pht_offset

    step = int((fc_target_utc - init_target_utc).total_seconds() / 3600)

    return {
        "date": init_target_utc.strftime("%Y%m%d"),
        "time": init_target_utc.strftime("%H%M"), 
        "step": step,                              
    }