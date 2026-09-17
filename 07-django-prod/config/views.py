from django.conf import settings
from django.http import JsonResponse


def home(request):
    return JsonResponse(
        {
            "ok": True,
            "mensaje": "Django servido con Gunicorn (modo producción)",
            "debug": settings.DEBUG,
        },
        json_dumps_params={"ensure_ascii": False},
    )
