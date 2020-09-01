import logging
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

logger = logging.getLogger(__name__)


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

        return Response({'payment_url': payment_url})

class YandexWebhook(APIView):
    payment_model = Payment

    def post(self, request, *args, **kwargs):
        """
        Endpoint for getting payment notifications from Yandex Checkout.
        """
        #TODO: using id from request, get Payment by external id,
        # update its' status if it's succesful
        logger.info(f"Got notification from Yandex.Checkout, payload: {request.data}")

        payment_object = request.data.get('object')
        if not payment_object:
            return Response({"msg": "No object data passed"}, status=status.HTTP_400_BAD_REQUEST)
        external_id = payment_object.get('id')

        # We want to blow up here if payment not found, to get error seen.
        afi_payment = Payment.objects.get(external_id=external_id)
        afi_payment.status = Payment.PAID
        afi_payment.save()
        return Response({"msg": "Got it!"}, status=status.HTTP_200_OK)


class PaymentMethodViewset(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    lookup_field = 'payment_type'
