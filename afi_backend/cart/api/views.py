from rest_framework import filters as drf_filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_json_api import (django_filters, filters, relations,
                                     serializers)

from rest_framework_json_api.views import viewsets
from afi_backend.cart.api.serializers import CartSerializer, OrderItemSerializer, CartOrderItemSerializer
from afi_backend.cart.models import Cart, OrderItem
from django.contrib.contenttypes.models import ContentType


class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.filter(is_paid=False)
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_fields = {
        'created_at': (
            'gt',
            'lt',
        ),
    }

    @action(detail=True,
            methods=["POST"],
            serializer_class=CartOrderItemSerializer,
            url_path='add-to-cart',
            permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        serializer = self.serializer_class(data=request.data)
        # To return correct type
        self.resource_name = 'Cart'

        if serializer.is_valid():
            serializer.save()
            cart.order_items.add(serializer.instance)
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=["POST"],
            serializer_class=CartOrderItemSerializer,
            url_path='buy-one',
            permission_classes=[IsAuthenticated])
    def buy_one(self, request):
        # TODO: DRY, create helper function, both methods are the same
        cart = Cart.objects.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            cart.order_items.add(serializer.instance)
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=["GET"],
            url_path='last-cart',
            permission_classes=[IsAuthenticated])
    def last_cart(self, pk=None):
        last_cart = Cart.latest_not_paid.all()
        return Response(self.serializer_class(last_cart).data)


class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_fields = {
        'created_at': (
            'gt',
            'lt',
        ),
    }
