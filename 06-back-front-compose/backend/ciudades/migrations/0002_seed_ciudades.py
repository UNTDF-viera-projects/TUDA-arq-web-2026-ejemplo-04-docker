from django.db import migrations

CIUDADES = [
    (
        "Ushuaia",
        "Capital provincial, sobre el canal Beagle. La ciudad más austral del mundo.",
        -54.8019,
        -68.303,
    ),
    (
        "Río Grande",
        "La ciudad más poblada de la provincia, sobre la costa del mar Argentino.",
        -53.7877,
        -67.7095,
    ),
    (
        "Tolhuin",
        "En el centro de la isla Grande, junto al lago Fagnano (Khami).",
        -54.5118,
        -67.1955,
    ),
]


def seed(apps, schema_editor):
    Ciudad = apps.get_model("ciudades", "Ciudad")
    for nombre, descripcion, lat, lng in CIUDADES:
        Ciudad.objects.get_or_create(
            nombre=nombre,
            defaults={"descripcion": descripcion, "lat": lat, "lng": lng},
        )


def unseed(apps, schema_editor):
    Ciudad = apps.get_model("ciudades", "Ciudad")
    Ciudad.objects.filter(nombre__in=[c[0] for c in CIUDADES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("ciudades", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
