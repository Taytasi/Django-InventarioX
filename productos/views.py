from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import productos
from rest_framework import viewsets
from .serializers import ProductoSerializer

def lista_productos(request):
    productos = productos.objects.all().values('id', 'nombre', 'precio', 'stock')
    return JsonResponse(list(productos), safe=False)

@csrf_exempt  # solo para demo; en producción manejar CSRF correctamente
def crear_producto_demo(request):
    # Crea un producto de demostración con datos fijos
    p = productos.objects.create(nombre="producto Demo", precio=1000.00, stock=10)
    return HttpResponse(f"producto creado: {p.id} - {p.nombre}")


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = productos.objects.all()
    serializer_class = ProductoSerializer