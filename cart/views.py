from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Count, F, Q
from products.models import Product
from .models import CartItem
from .serializers import CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProductListView(APIView):

    def get(self, request, *args, **kwargs):
        # Фильтрация продуктов по определенным условиям
        products = Product.objects.all()

        # Фильтрация продуктов по названию, если параметр title передан в запросе
        title = request.query_params.get('title', None)
        if title:
            products = products.filter(title__icontains=title)

        # Фильтрация по диапазону цен
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        if min_price or max_price:
            price_filters = {}
            if min_price:
                price_filters['price__gte'] = min_price
            if max_price:
                price_filters['price__lte'] = max_price
            products = products.filter(**price_filters)

        # Фильтрация по количеству на складе
        stock_threshold = request.query_params.get('stock_threshold', None)
        if stock_threshold:
            products = products.filter(stock__gte=stock_threshold)

        # Аннотирование дополнительных полей
        # Сумма цен продуктов
        products = products.annotate(total_price=Sum('price'))

        # Средняя цена
        products = products.annotate(average_price=Avg('price'))

        # Общее количество продуктов
        products = products.annotate(total_stock=Sum('stock'))

        # Продукты с ценой больше, чем количество, умноженное на 10 (использование F)
        products = products.annotate(price_to_stock_ratio=F('price') * F('stock'))

        # Получение результата с использованием aggregate
        aggregated_data = products.aggregate(
            total_price=Sum('price'),
            avg_price=Avg('price'),
            total_stock=Sum('stock'),
            total_products=Count('id')
        )

        # Применение фильтрации с использованием Q выражений
        # Например, продукты, которые либо дешевле 100, либо на складе меньше 10
        filtered_products = products.filter(
            Q(price__lte=100) | Q(stock__lt=10)
        )

        # Сериализация продуктов
        serializer = ProductSerializer(filtered_products, many=True)

        # Ответ с данными
        return Response({
            'products': serializer.data,
            'aggregated_data': aggregated_data
        })
