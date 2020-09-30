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
    queryset = Cart.objects.all()
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

    @action(detail=False,
            methods=["POST"],
            serializer_class=CartOrderItemSerializer,
            url_path='add-to-cart',
            permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        last_cart = Cart.objects.filter(customer=request.user,
                                        is_paid=False).last()
        if not last_cart:
            last_cart = Cart.objects.create(customer=request.user)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            last_cart.order_items.add(serializer.instance)
            last_cart_serializer = CartSerializer(last_cart)
            return Response(last_cart_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    # def create(self, request):
    #     # Create order item and link it to Cart
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     last_cart = Cart.objects.filter(customer=request.user,
    #                                     is_paid=False).last()
    #     if not last_cart:
    #         last_cart = Cart.objects.create(customer=request.user)

    #     last_cart.add(serializer.instance)

    #     return Response(status=status.HTTP_200_OK, data=serializer.data)
