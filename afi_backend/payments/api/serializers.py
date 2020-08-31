from rest_framework import serializers
from ..models import Payment, PaymentMethod


#TODO: display both number and human readable value

class PaymentMethodSerializer(serializers.ModelSerializer):
    payment_type_name = serializers.CharField(source='get_payment_type_display')
    payment_type_value = serializers.SerializerMethodField()

    class Meta:
        model = PaymentMethod
        fields = ['payment_type_name', 'payment_type_value',]

    def get_payment_type_value(self, obj):
        return obj.payment_type
