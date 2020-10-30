import logging

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from afi_backend.payments.api.serializers import (PaymentMethodSerializer,
    SubscriptionSerializer)
from afi_backend.payments.models import (Payment, PaymentMethod, Subscription, UserMembership,
    link_payment_with_cart)
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class PaymentCreateView(APIView):
    payment_model = Payment
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    @action(detail=False,
            methods=["POST"],
            url_path='get-payment-link',
            permission_classes=[IsAuthenticated])
    def get_payment_link(self, request):
        # Create payment link using payment adaptor.
        qs = UserMembership.objects.filter(user=request.user)
        serializer = None
        if qs.exists():  # Subscription exists.
            subscription = qs.first().subscription
            serializer = self.serializer_class(subscription, context={'user': request.user})
        else:  # Subscription doesn't exists, create it
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

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
                payment_method_id = payment_object["payment_method"]["id"]
                subscription = Subscription.objects.get(
                    external_id=external_id)
                subscription.is_active = True
                subscription.is_trial = False
                subscription.external_id = payment_method_id
                subscription.save()
                # TODO: schedule monthly payment task here
            except Subscription.DoesNotExist:
                return Response({"msg": "No such subscription"},
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
