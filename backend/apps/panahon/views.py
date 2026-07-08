from django.http import JsonResponse
from services.panahon.client import ( fetch_synoptic, fetch_aws )
from services.panahon.parser import ( parse_stations )


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