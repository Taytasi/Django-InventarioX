from rest_framework import serializers
from .models import productos

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = productos
        fields = "__all__"