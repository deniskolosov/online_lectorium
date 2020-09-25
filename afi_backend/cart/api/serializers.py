from rest_framework_json_api import serializers

from afi_backend.cart.models import Cart, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['content_object']


class CartSerializer(serializers.ModelSerializer):
    included_serializers = {'order_items': OrderItemSerializer}

    class Meta:
        model = Cart
        fields = [
            'order_items',
            'is_paid',
            'created_at',
        ]
