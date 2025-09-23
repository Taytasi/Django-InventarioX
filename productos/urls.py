from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('crear_demo/', views.crear_producto_demo, name='crear_producto_demo'),
]