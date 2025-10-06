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

# Valor por defecto para umbral; puedes mover a settings.py si quieres
REORDER_THRESHOLD = getattr(settings, "REORDER_THRESHOLD", 5)
DEFAULT_REORDER_QTY = getattr(settings, "DEFAULT_REORDER_QTY", 20)


# ✅ Página de inicio con hero
def inicio(request):
    return render(request, "inicio.html")


def productos(request):
    """
    Página cliente: lista productos. Maneja POST de creación si viene el formulario.
    Asigna una image_url a cada producto creado usando picsum.photos con seed basado en el id.
    """
    lista_productos = Producto.objects.all().order_by('id')

    # Crear producto desde formulario (POST)
    if request.method == 'POST' and 'create_product' in request.POST:
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            # Asignar imagen estable con seed basado en el id del producto
            try:
                producto.image_url = f"https://picsum.photos/seed/{producto.id}/400/300"
                producto.save(update_fields=['image_url'])
            except Exception:
                # en caso de error no bloqueamos la creación; dejamos image_url vacío
                pass

            messages.success(request, "Producto creado correctamente.")

            # Generar pedido si stock < umbral y no existe pedido no procesado
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
    """
    API ligera que devuelve lista de productos (JSON) incluyendo image_url.
    """
    productos = Producto.objects.all().values('id', 'nombre', 'precio', 'stock', 'image_url')
    return JsonResponse(list(productos), safe=False)


@csrf_exempt  # solo para demo; en producción manejar CSRF correctamente
def crear_producto_demo(request):
    """
    Crea un producto de demostración con datos fijos y asigna image_url.
    """
    p = Producto.objects.create(nombre="producto Demo", precio=1000.00, stock=10)
    try:
        p.image_url = f"https://picsum.photos/seed/{p.id}/400/300"
        p.save(update_fields=['image_url'])
    except Exception:
        pass
    return HttpResponse(f"producto creado: {p.id} - {p.nombre}")


def product_edit(request, pk):
    """
    Editar producto (página separada).
    Si image_url está vacío después de guardar, le asigna una URL con picsum basada en id.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            # Si no tiene imagen asignada, generarla ahora (estable por id)
            if not getattr(producto, 'image_url', None):
                try:
                    producto.image_url = f"https://picsum.photos/seed/{producto.id}/400/300"
                    producto.save(update_fields=['image_url'])
                except Exception:
                    pass

            messages.success(request, "Producto actualizado correctamente.")
            # Revisar stock y generar pedido si aplica
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
def product_delete(request, pk):
    """
    Eliminar producto (solo POST).
    """
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('productos')


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

