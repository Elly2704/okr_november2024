from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import F, Sum, Value, DecimalField, Case, When
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CartItem
from .serializers import CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user)  # filter by user
        product_title = self.request.query_params.get('product_title', None)  # filter by product_title

        if product_title:
            queryset = queryset.filter(product__title__icontains=product_title)

        queryset = queryset.annotate(
            discount=Case(
                When(product__price__gte=100, then=Value(0.10)),
                default=Value(0),
                output_field=DecimalField()
            )
        ).annotate(
            discounted_price=F('product__price') - (F('product__price') * F('discount'))
        ).annotate(
            total_price=F('quantity') * F('discounted_price')
        )
        return queryset

    @swagger_auto_schema(
        operation_summary="List cart items",
        operation_description="Returns cart items with calculated discounts and total sum.",
        tags=["Cart"],
        responses={200: openapi.Response("List of cart items", CartItemSerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_sum = queryset.aggregate(
            total_sum=Sum('total_price')
        )['total_sum']

        if total_sum is None:
            total_sum = 0

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'cart_items': serializer.data,
            'total_sum': total_sum
        })

    @swagger_auto_schema(
        operation_summary="Create cart item",
        operation_description="Create a new item in the cart.",
        tags=["Cart"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve cart item",
        operation_description="Retrieve a single cart item by ID.",
        tags=["Cart"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update cart item",
        operation_description="Update a cart item by ID.",
        tags=["Cart"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update cart item",
        operation_description="Partially update a cart item by ID.",
        tags=["Cart"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete cart item",
        operation_description="Delete a cart item by ID.",
        tags=["Cart"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
