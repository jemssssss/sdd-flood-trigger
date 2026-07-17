from django.http import JsonResponse
from services.panahon.client import ( fetch_synoptic, fetch_aws )
from services.panahon.parser import ( parse_stations )
from services.panahon.point import ( fetch_point_rainfall )
from services.panahon.footprint import ( compute_footprints )
from services.sentinel.passes import DEFAULT_SATELLITE

def synoptic(request):

    data = fetch_synoptic()
    parsed = parse_stations(
        data,
        "synoptic"
    )

    return JsonResponse(parsed, safe=False)

def aws(request):

    data = fetch_aws()
    parsed = parse_stations(
        data,
        "aws"
    )

    return JsonResponse(parsed, safe=False)

def point(request):

    required = [
        "lat",
        "lon",
        "t",
        "init",
    ]

    missing = [
        p for p in required
        if not request.GET.get(p)
    ]

    if missing:
        return JsonResponse(
            {
                "error": "Missing parameters",
                "missing": missing,
            },
            status=400,
        )

    rainfall = fetch_point_rainfall(
        lat=float(request.GET["lat"]),
        lon=float(request.GET["lon"]),
        forecast_time=request.GET["t"],
        init_time=request.GET["init"],
    )

    return JsonResponse(
        {
            "rainfall": rainfall
        }
    )

def footprints(request):

    forecast_time = request.GET.get("t")
    init_time = request.GET.get("init")
    satellite = request.GET.get("satellite", DEFAULT_SATELLITE)

    if not forecast_time or not init_time:

        return JsonResponse(
            {
                "error": "Missing t or init"
            },
            status=400,
        )

    try:
        result = compute_footprints(
            forecast_time,
            init_time,
            satellite,
        )
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse(result)
