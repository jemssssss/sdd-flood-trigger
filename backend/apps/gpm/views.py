from django.http import JsonResponse
from scripts.json_utils import to_python
from services.gpm.footprint import compute_gpm_footprints
from services.sentinel.passes import get_active_accumulation_window

# Get forecast_time and init_time

window = get_active_accumulation_window()
forecast = window["forecast"].isoformat()

def footprints(request):

    if not forecast:
    
        return JsonResponse(
            {
                "error": "Missing forecast_time",
            },
            status=400,
        )

    result = compute_gpm_footprints(
        forecast,
    )

    return JsonResponse(to_python(result))