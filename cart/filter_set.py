import django_filters
from .models import CartItem

class CartItemFilterSet(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    product = django_filters.CharFilter(field_name='product__title', lookup_expr='icontains')
    quantity = django_filters.RangeFilter()
    created_at = django_filters.DateFromToRangeFilter(field_name='product__created_at')

    class Meta:
        model = CartItem
        fields = ['user', 'product', 'quantity','created_at']
