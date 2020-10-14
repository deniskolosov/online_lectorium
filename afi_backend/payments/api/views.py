import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from afi_backend.payments.models import Payment, PaymentMethod, Subscription, link_payment_with_cart

from afi_backend.payments.api.serializers import PaymentMethodSerializer, SubscriptionSerializer

logger = logging.getLogger(__name__)


class PaymentCreateView(APIView):
    payment_model = Payment
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create Payment object for user for given item type, "Pending" status, currency and Payment Method.
        """
        required_fields = (
            'payment_type_value',
            'amount',
            'currency',
            'cart_id',
        )
        for val in required_fields:
            if val not in request.data:
                raise ValidationError(f"{val} field is  required")

        payment_type_value = request.data['payment_type_value']
        amount = request.data['amount']
        currency = request.data['currency']
        cart_id = request.data['cart_id']

        # Create Payment for cart
        payment = link_payment_with_cart(payment_type=payment_type_value,
                                         user=request.user,
                                         cart_id=cart_id)

        adaptor = payment.payment_method.get_adaptor()

        payment_url, external_id = adaptor.charge(
            value=amount,
            currency=currency,
            description=f'Payment #{payment.id}')
        payment.external_id = external_id
        payment.save()

        return Response({'payment_url': payment_url})


class CreateSubscriptionViewset(CreateModelMixin, GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @action(detail=True,
            methods=["POST"],
            url_path='get-payment-link',
            permission_classes=[IsAuthenticated])
    def get_payment_link(self, request, pk=None):
        # Create payment link using payment adaptor.

        required_fields = ('payment_type_value', )

        for val in required_fields:
            if val not in request.data:
                raise ValidationError(f"{val} field is  required")

        payment_type_value = request.data['payment_type_value']

        subscription = self.get_object()
        membership = subscription.user_membership.membership

        payment_method = PaymentMethod.objects.get(
            payment_type=payment_type_value)

        adaptor = payment_method.get_adaptor()

        payment_url, external_id = adaptor.charge(
            value=str(membership.price.amount),
            currency=membership.price.currency,
            description=f'Subscription #{subscription.id}',
            save_payment_method=True)
        subscription.external_id = external_id
        subscription.save()

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

        saved = payment_object["payment_method"]["saved"]

        if saved:  # Recurrent payment, use Subscription
            try:
                subscription = Subscription.objects.get(
                    external_id=external_id)
                subscription.is_active = True
                subscription.is_trial = False
                subscription.save()
            except Payment.DoesNotExist:
                return Response({"msg": "No such payment"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:  # normal payment, use Payment
            try:
                afi_payment = Payment.objects.get(external_id=external_id)
                afi_payment.status = Payment.STATUS.PAID
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
