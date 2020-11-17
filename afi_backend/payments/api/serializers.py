from rest_framework_json_api import serializers, relations
from afi_backend.payments.models import (Payment, PaymentMethod,
                                         VideoLectureOrderItem, Subscription,
                                         Membership, UserMembership)
from afi_backend.users.models import User


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
    class Meta:
        model = VideoLectureOrderItem
        fields = ['video_lecture']


class SubscriptionSerializer(serializers.ModelSerializer):
    membership_type = serializers.ChoiceField(
        choices=Membership.TIER,
        source='user_membership.membership.membership_type')
    payment_method = serializers.ChoiceField(
        choices=PaymentMethod.PAYMENT_TYPES,
        source='payment_method.payment_type',
    )
    payment_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'membership_type',
            'payment_method',
            'payment_url',
        ]

    def create(self, validated_data):
        membership = validated_data.get('user_membership')
        membership_type = membership.get('membership').get('membership_type')
        user = self.context['user']

        payment_type = validated_data.get('payment_method').get('payment_type')
        payment_method = PaymentMethod.objects.get(payment_type=payment_type)

        membership_type = Membership.objects.get(
            membership_type=membership_type)
        user_membership = UserMembership.objects.create(
            membership=membership_type, user=user)
        return Subscription.objects.create(user_membership=user_membership,
                                           payment_method=payment_method)

    def get_payment_url(self, obj):
        return obj.get_payment_url()


class MembershipField(relations.ResourceRelatedField):
    membership_type = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ['membership_type', 'price']

    def get_membership_type(self, obj):
        return obj.get_membership_type_display()


class UserMembershipSerializer(serializers.ModelSerializer):
    membership = MembershipField(read_only=True)

    class Meta:
        model = UserMembership
        fields = ['membership']
