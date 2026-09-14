from django.conf import settings
from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse


def estado_db(request):
    """Prueba real contra Postgres: si la red está bien, esto responde 200."""
    cfg = settings.DATABASES["default"]
    destino = {
        "host": cfg["HOST"],
        "port": cfg["PORT"],
        "name": cfg["NAME"],
        "user": cfg["USER"],
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), version(), now()")
            database, version, now = cursor.fetchone()
    except OperationalError as exc:
        connection.close()
        return JsonResponse(
            {
                "ok": False,
                "mensaje": "Django no pudo hablar con PostgreSQL",
                "destino": destino,
                "error": str(exc),
            },
            status=503,
            json_dumps_params={"ensure_ascii": False},
        )

    return JsonResponse(
        {
            "ok": True,
            "mensaje": "Django se conectó a PostgreSQL",
            "destino": destino,
            "database": database,
            "postgres": version,
            "ahora": now.isoformat(),
        },
        json_dumps_params={"ensure_ascii": False},
    )
