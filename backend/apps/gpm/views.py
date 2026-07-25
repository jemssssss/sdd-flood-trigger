from django.http import JsonResponse
from scripts.json_utils import to_python
from services.gpm.footprint import compute_gpm_footprints

def footprints(request):

    forecast = request.GET.get("t")

    result = compute_gpm_footprints(
        forecast,
    )

    return JsonResponse(to_python(result))