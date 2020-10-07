from rest_framework_json_api import serializers

from afi_backend.cart.models import Cart, OrderItem
from afi_backend.events.models import VideoLecture
from afi_backend.tickets.models import Ticket
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Sum


class OrderItemRelatedField(ResourceRelatedField):
    def to_representation(self, value):
        """
        Serialize order_items to a simple textual representation.
        """
        if isinstance(value, VideoLecture):
            return f'Video Lecture id#{value.id}'
        if isinstance(value, Ticket):
            return f'Ticket #id {value.id}'
        raise Exception('Unexpected type of order_item')


class OrderItemSerializer(serializers.ModelSerializer):
    content_object = OrderItemRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['created_at', 'content_object']


class CartSerializer(serializers.ModelSerializer):
    included_serializers = {'order_items': OrderItemSerializer}
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'order_items',
            'is_paid',
            'created_at',
            'total',
        ]

    def get_total(self, obj):
        total = 0
        for item in obj.order_items.all():
            price = None
            if item.content_object:
                price = item.content_object.price
            if price:
                total += price

        if total:
            return total.amount
        return None


class CartOrderItemSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField()
    object_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['item_type', 'object_id']

    def create(self, validated_data):
        content_type = ContentType.objects.get(
            model=validated_data['item_type'])

        order_item = OrderItem.objects.create(
            content_type=content_type, object_id=validated_data['object_id'])

        return order_item
