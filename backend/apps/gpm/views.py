from django.http import JsonResponse
from scripts.json_utils import to_python
from services.gpm.footprint import compute_gpm_footprints
from services.sentinel.passes import DEFAULT_SATELLITE

def footprints(request):

    forecast = request.GET.get("t")

    satellite = request.GET.get(
        "satellite",
        DEFAULT_SATELLITE,
    )

    result = compute_gpm_footprints(
        forecast,
        satellite,
    )

    return JsonResponse(to_python(result))