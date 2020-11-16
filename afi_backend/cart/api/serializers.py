from rest_framework_json_api import serializers

from afi_backend.cart.models import Cart, OrderItem
from afi_backend.events.models import VideoLecture
from afi_backend.tickets.models import Ticket
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Sum
from afi_backend.events.api.serializers import VideoLectureSerializer, OfflineLectureSerializer, LecturerSerializer
from afi_backend.tickets.api.serializers import TicketSerializer
from afi_backend.videocourses.api.serializers import VideoCourseSerializer
from afi_backend.videocourses.models import VideoCourse
from afi_backend.users.models import User
from afi_backend.packages.models import VideoCoursePackage, VideoLecturePackage
from afi_backend.packages.api.serializers import VideoCoursePackageSerializer, VideoLecturePackageSerializer


class OrderItemRelatedField(ResourceRelatedField):
    def to_representation(self, value):
        """
        Serialize order_items by their type.
        # TODO: DRY! refactor
        """
        if isinstance(value, VideoLecture):
            data = VideoLectureSerializer(value).data
            data["type"] = "VideoLecture"
            # TODO: OPTIMIZE ME!
            data["lecturer"] = LecturerSerializer(value.lecturer).data
            return data

        if isinstance(value, Ticket):
            data = TicketSerializer(value).data
            data["type"] = "Ticket"
            # TODO: OPTIMIZE ME!
            data["offline_lecture"] = OfflineLectureSerializer(
                value.offline_lecture).data
            return data

        if isinstance(value, VideoCourse):
            data = VideoCourseSerializer(value).data
            data["type"] = "VideoCourse"
            return data

        if isinstance(value, VideoCoursePackage):
            video_courses = value.videocourses
            data = VideoCourseSerializer(video_courses, many=True).data
            for val in data:
                val['type'] = 'VideoCourse'
            return data

        if isinstance(value, VideoLecturePackage):
            video_lectures = value.videolectures
            data = VideoLectureSerializer(video_lectures, many=True).data
            for val in data:
                val['type'] = 'VideoLecture'
            return data

        raise Exception('Unexpected type of order_item')


class OrderItemSerializer(serializers.ModelSerializer):
    content_object = OrderItemRelatedField(read_only=True)
    included_serializers = {
        'offline_lectures': OfflineLectureSerializer,
    }

    class Meta:
        model = OrderItem
        fields = ['created_at', 'content_object', 'is_paid']


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
    customer_email = serializers.EmailField()

    class Meta:
        model = OrderItem
        fields = ['item_type', 'object_id', 'customer_email']

    def create(self, validated_data):
        content_type = ContentType.objects.get(
            model=validated_data['item_type'])

        user = User.objects.get(email=validated_data['customer_email'])

        order_item = OrderItem.objects.create(
            customer=user,
            content_type=content_type,
            object_id=validated_data['object_id'])

        return order_item
