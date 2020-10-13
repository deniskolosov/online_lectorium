from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status, parsers, response
from rest_framework.decorators import action, parser_classes
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from afi_backend.cart.api.serializers import OrderItemSerializer
from rest_framework import filters as drf_filters
from rest_framework_json_api import django_filters as dj_filters
from rest_framework_json_api import filters
from afi_backend.users.api.serializers import UserSerializer, UserpicSerializer
from django_filters import rest_framework as django_filters_filters
from afi_backend.cart.models import OrderItem

User = get_user_model()


class ItemTypeFilter(django_filters_filters.FilterSet):
    item_type = django_filters_filters.CharFilter(
        field_name='order_items__content_type__model', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['item_type']


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "email"
    lookup_value_regex = "[^/]+"
    filter_backends = (
        filters.QueryParameterValidationFilter,
        dj_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_class = ItemTypeFilter

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True,
            methods=["PUT"],
            serializer_class=UserpicSerializer,
            url_path='upload-userpic',
            url_name='upload_userpic',
            permission_classes=[IsAuthenticated])
    @parser_classes([parsers.MultiPartParser])
    def upload_userpic(self, request, email=None):
        obj = self.get_object()
        serializer = self.serializer_class(obj,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["GET"],
        url_path='purchased-items',
        url_name='purchased-items',
        serializer_class=OrderItemSerializer,
        permission_classes=[IsAuthenticated],
    )
    def purchased_items(self, request, email=None):
        # todo: refactor filters
        obj = User.objects.get(email=email)
        queryset = obj.order_items.filter(is_paid=True)
        item_type = request.GET.get('filter[item_type]')
        lecturer_id = request.GET.get('filter[lecturer.id]')
        search = request.GET.get('filter[search]')

        if item_type:
            queryset = queryset.filter(content_type__model=item_type)

        if lecturer_id:
            queryset = queryset.filter(
                (Q(content_type__model='videolecture')
                 & Q(video_lecture__lecturer__id=lecturer_id))
                | (Q(content_type__model='videocourse')
                   & Q(video_course__lecturer__id=lecturer_id)))

        if search:
            queryset = queryset.filter(
                Q(video_lecture__name__icontains=search)
                | Q(video_lecture__description__icontains=search)
                | Q(ticket__offline_lecture__description__icontains=search)
                | Q(ticket__offline_lecture__name__icontains=search)
                | Q(video_course__name__icontains=search))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
