from django.urls import path

from . import views

urlpatterns = [
    path("ciudades/", views.listar_ciudades),
]
