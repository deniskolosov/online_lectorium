import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from ..models import Payment, PaymentMethod
from .serializers import PaymentMethodSerializer

logger = logging.getLogger(__name__)


class PaymentCreateView(APIView):
    payment_model = Payment
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create Payment object for user for given item type, "Pending" status, currency and Payment Method
        """
        if 'payment_type_value' not in request.data:
            raise ValidationError("'payment_type_value' field is required.")

        if 'payment_for' not in request.data:
            raise ValidationError("'payment for' field is required.")

        payment_method = PaymentMethod.objects.get(
            payment_type=request.data['payment_type_value'])

        payment_for = ContentType.objects.get(
            model=request.data['payment_for'])

        adaptor = payment_method.get_adaptor()

        # TODO: Raise validation error if any of this is not present.
        # TODO create variable for request data
        amount = request.data['amount']
        currency = request.data['currency']

        payment = self.payment_model.objects.create(
            user=self.request.user,
            payment_method=payment_method,
            payment_for=payment_for,
            object_id=request.data['object_id'])

        payment_url = adaptor.charge(value=amount,
                                     currency=currency,
                                     description='Change me',
                                     internal_payment_id=payment.id)

        return Response({'payment_url': payment_url})


class YandexWebhook(APIView):
    payment_model = Payment
    permission_classes = []
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        """
        Endpoint for getting payment notifications from Yandex Checkout.
        """
        logger.info(
            f"Got notification from Yandex.Checkout, payload: {request.data}")

        payment_object = request.data.get('object')
        if not payment_object:
            return Response({"msg": "No object data passed"},
                            status=status.HTTP_400_BAD_REQUEST)
        external_id = payment_object.get('id')

        try:
            afi_payment = Payment.objects.get(external_id=external_id)
            afi_payment.status = Payment.PAID
            afi_payment.save()
        except Payment.DoesNotExist:
            return Response({"msg": "No such payment"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "Got it!"}, status=status.HTTP_200_OK)


class CloudpaymentsWebhook(APIView):
    payment_model = Payment
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Endpoint for getting payment notifications from Cloudpayments.
        """
        logger.info(
            f"Got payment notification from Cloudpayments, payload: {request.data}"
        )

        data = request.data
        if not data:
            return Response({"msg": "No data passed"},
                            status=status.HTTP_400_BAD_REQUEST)
        payment_id = data.get('InvoiceId')

        try:
            afi_payment = Payment.objects.get(id=payment_id)
            afi_payment.status = Payment.STATUS.PAID
            afi_payment.save()
        except Payment.DoesNotExist:
            return Response({"msg": "No such payment"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"code": 0}, status=status.HTTP_200_OK)


class PaymentMethodViewset(RetrieveModelMixin, ListModelMixin,
                           UpdateModelMixin, GenericViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    lookup_field = 'payment_type'
