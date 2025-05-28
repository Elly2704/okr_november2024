from rest_framework import serializers
from .models import CartItem, User
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    discount = serializers.DecimalField(
        read_only=True,
        max_digits=5,
        decimal_places=2,
        help_text="Discount amount in fractions (for example, 0.10 = 10%)"
    )
    discounted_price = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2,
        help_text="Product price with discount"
    )
    total_price = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2,
        help_text="Total price for the item, taking into account quantity and discount"
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="ID of the user who owns the cart item"
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        help_text="ID of the product to add to cart"
    )


    class Meta:
        model = CartItem
        fields = [
            'id',
            'user',
            'product',
            'quantity',
            'discount',
            'discounted_price',
            'total_price'
        ]
        read_only_fields = ['id', 'user', 'discount', 'discounted_price', 'total_price']
