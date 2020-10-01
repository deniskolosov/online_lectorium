from rest_framework import serializers
from afi_backend.payments.models import Payment, PaymentMethod, VideoLectureOrderItem
from afi_backend.events.api.serializers import VideoLectureSerializer

#TODO: display both number and human readable value


class PaymentMethodSerializer(serializers.ModelSerializer):
    payment_type_name = serializers.CharField(
        source='get_payment_type_display')
    payment_type_value = serializers.SerializerMethodField()

    class Meta:
        model = PaymentMethod
        fields = [
            'payment_type_name',
            'payment_type_value',
        ]

    def get_payment_type_value(self, obj):
        return obj.payment_type


class VideoLectureOrderItemSerializer(serializers.ModelSerializer):
    video_lecture = VideoLectureSerializer()

    class Meta:
        model = VideoLectureOrderItem
        fields = ['video_lecture']
