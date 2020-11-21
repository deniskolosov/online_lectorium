import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from djoser.conf import settings as djoser_settings
from django.db.models import Q
from django_filters import rest_framework as django_filters_filters
from djoser import views as djoser_views
from djoser import utils
from rest_framework import filters as drf_filters, parsers, response, status
from rest_framework.decorators import action, parser_classes
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_json_api import django_filters as dj_filters, filters
from rest_framework_json_api import renderers

from djoser import signals, utils
from djoser.compat import get_user_email

from afi_backend.cart.api.serializers import OrderItemSerializer
from afi_backend.cart.models import OrderItem
from afi_backend.users.api.serializers import (UserSerializer,
                                               UserpicSerializer)

User = get_user_model()


class ItemTypeFilter(django_filters_filters.FilterSet):
    item_type = django_filters_filters.CharFilter(
        field_name='order_items__content_type__model', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['item_type']


class UserViewSet(djoser_views.UserViewSet):
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

    @action(["get"],
            detail=False,
            url_path=('activation/(?P<uid>\d+)/(?P<token>[^/.]+)/'))
    def activation(self, request: Request, uid: str, token: str, *args,
                   **kwargs) -> Response:
        serializer = self.get_serializer(data={"uid": uid, "token": token})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(sender=self.__class__,
                                    user=user,
                                    request=self.request)

        if djoser_settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            djoser_settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

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


# Reroute activation link request to djoser api
class ActivateUser(GenericAPIView):
    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}

        url = "/api/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())
