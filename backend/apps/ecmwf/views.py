from django.http import JsonResponse
from services.ecmwf.footprint import (compute_ecmwf_footprints)
from services.ecmwf.json_utils import to_python

def footprints(request):

    forecast = request.GET.get("t")
    init = request.GET.get("init")

    if not forecast or not init:

        return JsonResponse(
            {
                "error": "Missing t or init",
            },
            status=400,
        )

    result = compute_ecmwf_footprints(
        forecast,
        init,
    )

    return JsonResponse(to_python(result))