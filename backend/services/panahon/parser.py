def parse_stations(raw_data, station_type="synoptic"):

    items = (
        raw_data
        if isinstance(raw_data, list)
        else raw_data.get("data", [])
    )

    stations = []

    for index, item in enumerate(items):

        lat = item.get("latitude") or item.get("lat")
        lon = item.get("longitude") or item.get("lon") or item.get("lng")

        if lat is None or lon is None:
            continue

        lat = float(lat)
        lon = float(lon)

        rainfall = (
            float(item.get("24_hr_value", 0))
            if station_type == "aws"
            else float(item.get("value", 0))
        )

        stations.append({

            "id":
                item.get("id")
                or item.get("site_id")
                or f"station-{index}",

            "stationName":
                item.get("stationName")
                or item.get("site_name")
                or "Unknown Station",

            "latitude": lat,
            "longitude": lon,

            "rainfallMm": rainfall,

            "observedAt":
                item.get("observedAt")
                or item.get("observed_at"),

            "stationType": station_type,

        })

    return stations