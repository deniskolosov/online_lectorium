from rest_framework_json_api import serializers

from afi_backend.cart.models import Cart, OrderItem
from afi_backend.events.models import VideoLecture
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Sum


class OrderItemRelatedField(ResourceRelatedField):
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, VideoLecture):
            return 'Video Lecture ' + value.name
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
        return obj.order_items.annotate(
            v_price=F('video_lecture__price'),
            t_price=F('ticket__offline_lecture__price')).aggregate(
                total=Sum('v_price') + Sum('t_price'))['total']


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
            item=content_type, object_id=validated_data['object_id'])

        return order_item
