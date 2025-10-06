from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("productos/", views.productos, name="productos"),
    path("productos/<int:pk>/edit/", views.product_edit, name="producto_edit"),
    path("productos/<int:pk>/delete/", views.product_delete, name="producto_delete"),
    path("api/lista/", views.lista_productos, name="api_lista_productos"),
    path("api/crear-demo/", views.crear_producto_demo, name="api_crear_demo"),
]

