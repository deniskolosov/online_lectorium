from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Payment, PaymentMethod
from .serializers import PaymentMethodSerializer
from rest_framework.views import APIView


class PaymentCreateView(APIView):
    payment_model = Payment

    def post(self, request, *args, **kwargs):
        """
        Create Payment object for user for given item type, "Pending" status, currency and Payment Method
        """
        if 'payment_type_value' not in request.data:
            raise ValidationError("'payment_type_value' field is required.")

        payment_method = PaymentMethod.objects.get(payment_type=request.data['payment_type_value'])
        adaptor = payment_method.get_adaptor()
        # TODO: Raise validation error if any of this is not present.
        amount = request.data['amount']
        currency = request.data['currency']


        payment = self.payment_model.objects.create(user=self.request.user, payment_method=payment_method)
        payment_url = adaptor.charge(value=amount, currency=currency, description=f'Change me', internal_payment_id=payment.id)

        # TODO: Check how to document a response and document it
        return Response({'payment_url': payment_url})

class PaymentMethodViewset(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    lookup_field = 'payment_type'
