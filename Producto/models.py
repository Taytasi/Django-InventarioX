from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.precio}"

    class Meta:
        db_table = "producto_producto"


class PedidoReabastecimiento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="pedidos_reabastecimiento")
    cantidad_sugerida = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido de {self.producto.nombre} ({self.cantidad_sugerida} unidades)"

    class Meta:
        db_table = "pedido_reabastecimiento"


