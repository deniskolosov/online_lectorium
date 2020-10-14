from rest_framework_json_api import serializers
from afi_backend.payments.models import Payment, PaymentMethod, VideoLectureOrderItem, Subscription, Membership, UserMembership
from afi_backend.events.api.serializers import VideoLectureSerializer
from afi_backend.users.models import User

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


class SubscriptionSerializer(serializers.ModelSerializer):
    membership_type = serializers.ChoiceField(
        choices=Membership.TIER,
        source='user_membership.membership.membership_type')
    user_id = serializers.IntegerField(source='user_membership.user.id')

    class Meta:
        model = Subscription
        fields = ['membership_type', 'user_id']

    def create(self, validated_data):
        membership = validated_data.get('user_membership')
        membership_type = membership.get('membership').get('membership_type')
        user_data = membership.get('user')
        user = User.objects.get(id=user_data.get('id'))
        membership_type = Membership.objects.get(
            membership_type=membership_type)
        user_membership = UserMembership.objects.create(
            membership=membership_type, user=user)
        return Subscription.objects.create(user_membership=user_membership)
