"""
URL configuration for INVENTARIOX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Producto.views import ProductoViewSet, register

# Rutas de la API con DRF
router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # App principal
    path('', include('Producto.urls')),

    # API REST
    path('api/', include(router.urls)),

    # Autenticación integrada de Django (login, logout, reset password, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Registro personalizado
    path('accounts/register/', register, name='register'),
]


