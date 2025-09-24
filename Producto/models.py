from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.precio}"

    class Meta:
        db_table = "producto_producto"  # 👈 nombre exacto de mi tabla en MySQL


