from django.urls import path

from . import views

urlpatterns = [
    path("", views.estado_db),
]
