import django_filters
from products.models import Product


class ProductFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains') # case insensitive
    brand = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.RangeFilter()
    stock = django_filters.NumberFilter(lookup_expr='exact')
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Product
        fields = ['id', 'title', 'brand', 'description', 'price', 'stock', 'created_at']
