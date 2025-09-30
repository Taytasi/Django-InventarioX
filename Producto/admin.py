from django.contrib import admin, messages
from django.utils.html import format_html
from import_export.admin import ExportMixin
from django.http import HttpResponse
import csv
from .models import Producto, PedidoReabastecimiento  # 👈 importamos el nuevo modelo

@admin.register(Producto)
class ProductoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'stock', 'estado_stock')
    search_fields = ('nombre',)
    list_filter = ('precio',)
    actions = ['generar_pedido_reabastecimiento', 'exportar_informe_inventario']  # 👈 añadimos la nueva acción

    # 🔹 Columna con alerta de stock en la lista
    def estado_stock(self, obj):
        if obj.stock < 5:
            return format_html('<span style="color: red; font-weight: bold;">⚠ Stock Bajo ({})</span>', obj.stock)
        return format_html('<span style="color: green;">{}</span>', obj.stock)
    
    estado_stock.short_description = "Alerta de Stock"

    # 🔹 Mensaje de advertencia al abrir el producto
    def change_view(self, request, object_id, form_url='', extra_context=None):
        producto = self.get_object(request, object_id)
        if producto and producto.stock < 5:
            self.message_user(
                request,
                f"⚠ El producto '{producto.nombre}' tiene un stock bajo ({producto.stock} unidades).",
                level=messages.WARNING
            )
        return super().change_view(request, object_id, form_url, extra_context)

    # 🔹 Acción: generar pedido de reabastecimiento
    def generar_pedido_reabastecimiento(self, request, queryset):
        pedidos_creados = 0
        for producto in queryset:
            if producto.stock < 5:  # umbral de stock
                PedidoReabastecimiento.objects.create(
                    producto=producto,
                    cantidad_sugerida=20  # 👈 aquí defines la cantidad sugerida
                )
                pedidos_creados += 1
        self.message_user(request, f"✅ Se generaron {pedidos_creados} pedidos de reabastecimiento.")
    generar_pedido_reabastecimiento.short_description = "Generar pedido de reabastecimiento"

    # 🔹 Acción: exportar informe de inventario en CSV
    def exportar_informe_inventario(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="informe_inventario.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nombre', 'Precio', 'Stock'])

        for producto in queryset:
            writer.writerow([producto.id, producto.nombre, producto.precio, producto.stock])

        self.message_user(request, f"✅ Informe de inventario generado con {queryset.count()} productos.")
        return response
    exportar_informe_inventario.short_description = "Exportar informe de inventario (CSV)"


# 👇 Registrar también el modelo PedidoReabastecimiento en el admin
@admin.register(PedidoReabastecimiento)
class PedidoReabastecimientoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_sugerida', 'fecha', 'procesado')
    list_filter = ('procesado', 'fecha')
    search_fields = ('producto__nombre',)

    
    

