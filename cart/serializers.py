from rest_framework import serializers
from .models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

# from rest_framework import serializers
# from .models import CartItem
#
# class CartItemSerializer(serializers.ModelSerializer):
#     discount = serializers.DecimalField(
#         read_only=True, max_digits=5, decimal_places=2,
#         help_text="Discount amount in fractions (for example, 0.10 = 10%)"
#     )
#     discounted_price = serializers.DecimalField(
#         read_only=True, max_digits=10, decimal_places=2,
#         help_text="Product price with discount"
#     )
#     total_price = serializers.DecimalField(
#         read_only=True, max_digits=10, decimal_places=2,
#         help_text="Total price for the item, taking into account quantity and discount"
#     )
#     user = serializers.StringRelatedField(read_only=True)
#     product = serializers.StringRelatedField(read_only=True)
#
#     class Meta:
#         model = CartItem
#         fields = [
#             'id',
#             'user',
#             'product',
#             'quantity',
#             'discount',
#             'discounted_price',
#             'total_price'
#         ]
#         read_only_fields = ['id', 'user', 'discount', 'discounted_price', 'total_price']
