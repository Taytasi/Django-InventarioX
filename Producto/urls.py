from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),  # Ruta para la página principal
    path("productos/", views.productos, name="productos"),  # Ruta para productos
]