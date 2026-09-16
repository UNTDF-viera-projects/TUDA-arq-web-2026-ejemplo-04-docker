from django.http import JsonResponse

from .models import Ciudad


def listar_ciudades(request):
    ciudades = [
        {
            "nombre": ciudad.nombre,
            "descripcion": ciudad.descripcion,
            "lat": ciudad.lat,
            "lng": ciudad.lng,
        }
        for ciudad in Ciudad.objects.all()
    ]
    return JsonResponse(
        {
            "provincia": "Tierra del Fuego, Antártida e Islas del Atlántico Sur",
            "pais": "Argentina",
            "ciudades": ciudades,
        },
        json_dumps_params={"ensure_ascii": False},
    )
