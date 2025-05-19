from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import F
from .models import Product
from .serializers import ProductSerializer

@extend_schema(summary='CRUD for products',
                   description="This endpoints allows to get list of products, get product by id, create product, update product, delete product",
                   request=ProductSerializer,
                   tags=["Products"]
                   )
class ProductViewSet(viewsets.ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        def get_queryset(self):
            queryset = Product.objects.all()
            queryset = queryset.annotate(stock_amount=F('stock')).filter(stock_amount__gt=0)

            return queryset

        def get_permissions(self):
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                return [IsAdminUser()]
            else:
                return [AllowAny()]



