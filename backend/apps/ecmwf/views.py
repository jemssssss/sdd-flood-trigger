from django.http import JsonResponse
from services.ecmwf.footprint import (compute_ecmwf_footprints)
from services.ecmwf.json_utils import to_python
from services.sentinel.passes import DEFAULT_SATELLITE

def footprints(request):

    forecast = request.GET.get("t")
    init = request.GET.get("init")
    satellite = request.GET.get("satellite", DEFAULT_SATELLITE)

    if not forecast or not init:

        return JsonResponse(
            {
                "error": "Missing t or init",
            },
            status=400,
        )

    try:
        result = compute_ecmwf_footprints(
            forecast,
            init,
            satellite,
        )
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse(to_python(result))
