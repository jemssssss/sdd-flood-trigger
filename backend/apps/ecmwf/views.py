from django.http import JsonResponse
from services.ecmwf.footprint import compute_ecmwf_footprints
from services.sentinel.passes import get_active_accumulation_window
from scripts.json_utils import to_python

# Get forecast_time and init_time

window = get_active_accumulation_window()

forecast = window["forecast"].isoformat()
init = (
    window["init"]
    .isoformat()
    .replace("+00:00", "Z")
)

def footprints(request):

    if not forecast or not init:

        return JsonResponse(
            {
                "error": "Missing forecast_time or init_time",
            },
            status=400,
        )

    try:
        result = compute_ecmwf_footprints(
            forecast,
            init,
        )
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse(to_python(result))
