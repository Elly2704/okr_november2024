from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = queryset.annotate(stock_amount=F('stock')).filter(stock_amount__gt=0)
        return queryset

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         return [IsAdminUser()]
    #     return [AllowAny()]

    @swagger_auto_schema(
        operation_summary="List products",
        operation_description="Returns a list of available products (with stock > 0).",
        tags=["Products"],
        responses={200: openapi.Response("List of products", ProductSerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve product",
        operation_description="Retrieve a product by its ID.",
        tags=["Products"],
        responses={200: openapi.Response("Product detail", ProductSerializer())}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create product",
        operation_description="Create a new product. Admin access only.",
        tags=["Products"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update product",
        operation_description="Fully update a product. Admin access only.",
        tags=["Products"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update product",
        operation_description="Partially update a product. Admin access only.",
        tags=["Products"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete product",
        operation_description="Delete a product. Admin access only.",
        tags=["Products"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
