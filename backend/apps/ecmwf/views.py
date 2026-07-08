from django.http import JsonResponse
from django.views.decorators.http import require_GET
from services.ecmwf.point import get_ecmwf_point_value

@require_GET
def point(request): 
    required_params = [
        "url", 
        "t", 
        "lon", 
        "lat", 
        "init"
    ] 
    
    missing = [
        name for name in required_params if not request.GET.get(name)
    ] 
    
    if missing: 
        return JsonResponse({ 
            "error": "Missing required query parameters.", 
            "missing": missing, 
        }, status=400) 
    
    url = request.GET["url"] 
    t = request.GET["t"] 
    init = request.GET["init"] 

    try: 
        lon = float(request.GET["lon"]) 
        lat = float(request.GET["lat"]) 
    except ValueError: 
        return JsonResponse({ 
            "error": "lon and lat must be valid numbers.", 
        }, status=400)
    
    result = get_ecmwf_point_value( 
        url=url, 
        t=t, 
        lon=lon, 
        lat=lat, 
        init=init, 
    )

    return JsonResponse(result)