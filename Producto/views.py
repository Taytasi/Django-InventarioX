# Producto/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.http import require_POST

from rest_framework import viewsets
from .serializers import ProductoSerializer

from .models import Producto, PedidoReabastecimiento
from .forms import ProductoForm
from django.conf import settings

# 🔑 NUEVOS IMPORTS
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Valor por defecto para umbral
REORDER_THRESHOLD = getattr(settings, "REORDER_THRESHOLD", 5)
DEFAULT_REORDER_QTY = getattr(settings, "DEFAULT_REORDER_QTY", 20)


def inicio(request):
    return render(request, "inicio.html")


# 🔑 PROTEGER esta vista con login_required
@login_required
def productos(request):
    lista_productos = Producto.objects.all().order_by('id')

    if request.method == 'POST' and 'create_product' in request.POST:
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            try:
                producto.image_url = f"https://picsum.photos/seed/{producto.id}/400/300"
                producto.save(update_fields=['image_url'])
            except Exception:
                pass

            messages.success(request, "Producto creado correctamente.")

            if producto.stock < REORDER_THRESHOLD:
                existe = PedidoReabastecimiento.objects.filter(producto=producto, procesado=False).exists()
                if not existe:
                    PedidoReabastecimiento.objects.create(producto=producto, cantidad_sugerida=DEFAULT_REORDER_QTY)
                    messages.info(request, "Se generó un pedido de reabastecimiento automático (stock bajo).")

            return redirect('productos')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    else:
        form = ProductoForm()

    return render(request, "productos.html", {"productos": lista_productos, "form": form})


def lista_productos(request):
    productos = Producto.objects.all().values('id', 'nombre', 'precio', 'stock', 'image_url')
    return JsonResponse(list(productos), safe=False)


@csrf_exempt
def crear_producto_demo(request):
    p = Producto.objects.create(nombre="producto Demo", precio=1000.00, stock=10)
    try:
        p.image_url = f"https://picsum.photos/seed/{p.id}/400/300"
        p.save(update_fields=['image_url'])
    except Exception:
        pass
    return HttpResponse(f"producto creado: {p.id} - {p.nombre}")


@login_required
def product_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            if not getattr(producto, 'image_url', None):
                try:
                    producto.image_url = f"https://picsum.photos/seed/{producto.id}/400/300"
                    producto.save(update_fields=['image_url'])
                except Exception:
                    pass

            messages.success(request, "Producto actualizado correctamente.")
            if producto.stock < REORDER_THRESHOLD:
                existe = PedidoReabastecimiento.objects.filter(producto=producto, procesado=False).exists()
                if not existe:
                    PedidoReabastecimiento.objects.create(producto=producto, cantidad_sugerida=DEFAULT_REORDER_QTY)
                    messages.info(request, "Se generó un pedido de reabastecimiento automático (stock bajo).")
            return redirect('productos')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'product_form.html', {'form': form, 'producto': producto})


@require_POST
@login_required
def product_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('productos')


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# 🔑 NUEVA VISTA DE REGISTRO
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # iniciar sesión automáticamente
            messages.success(request, "Cuenta creada correctamente. Bienvenido!")
            return redirect('productos')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


