from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import F, Sum, Value, DecimalField, Case, When
from .models import CartItem
from .serializers import CartItemSerializer

@extend_schema(summary='CRUD for cart items',
                   description="This endpoints for viewing and editing items in the cart. Provides full CRUD functionality for the CartItem model.",
                   request=CartItemSerializer,
                   tags=["Cart"]
                   )
class CartViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user) #filter by user
        product_title = self.request.query_params.get('product_title', None)#filter by product_title

        if product_title:
            queryset = queryset.filter(product__title__icontains=product_title)  #search by product

        #queryset = queryset.annotate(total_price=F('quantity') * F('product__price'))

        queryset = queryset.annotate(
            discount=Case(
                When(product__price__gte=100, then=Value(0.10)),  # 10% discount
                default=Value(0),  #without discount
                output_field=DecimalField()
            )
        ).annotate(
            discounted_price=F('product__price') - (F('product__price') * F('discount'))
        ).annotate(
            total_price=F('quantity') * F('discounted_price')  #recalculate total price
        )
        return queryset

    @extend_schema(summary='Total sum for products in cart',
                   description="This endpoint shows the total sum in cart",
                   request=CartItemSerializer,
                   tags=["Cart"]
                   )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_sum = queryset.aggregate(total_sum=Sum(F('quantity') * F('product__price')))['total_sum']

        if total_sum is None:
            total_sum = 0

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'cart_items': serializer.data,
            'total_sum': total_sum
        })