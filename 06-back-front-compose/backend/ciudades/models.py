from django.db import models


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
