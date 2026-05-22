from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    # Ordena pelo código do produto
    queryset = Product.objects.all().order_by("code")
    serializer_class = ProductSerializer
