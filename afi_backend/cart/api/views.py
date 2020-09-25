from rest_framework import filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import (django_filters, filters, relations,
                                     serializers)

from rest_framework_json_api.views import viewsets
from afi_backend.cart.api.serializers import CartSerializer
from afi_backend.cart.models import Cart


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
