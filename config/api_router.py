from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from afi_backend.events.api.views import (
    LecturersViewset,
    OfflineLectureViewset,
    CategoriesViewSet,
    VideoLectureViewset,
)
from afi_backend.payments.api.views import (
    CloudpaymentsWebhook,
    PaymentCreateView,
    PaymentMethodViewset,
    YandexWebhook,
    CreateSubscriptionViewset,
)
from afi_backend.tickets.api.views import TicketViewSet
from afi_backend.users.api.views import UserViewSet
from afi_backend.cart.api.views import CartViewset, OrderItemViewset
from afi_backend.videocourses.api.views import VideoCourseViewset
from afi_backend.blog.api.views import PostViewset

class OptionalSlashRouter(SimpleRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

if settings.DEBUG:
    router = OptionalSlashRouter()
else:
    router = OptionalSlashRouter()

router.register("users", UserViewSet)
router.register("payment_methods",
                PaymentMethodViewset,
                basename='payment-methods')
router.register("tickets", TicketViewSet, basename='tickets')
router.register("offline-lectures",
                OfflineLectureViewset,
                basename='offline-lectures')
router.register("video-lectures",
                VideoLectureViewset,
                basename='video-lectures')
router.register("videocourses", VideoCourseViewset, basename='videocourses')
router.register("cart", CartViewset, basename='cart')
router.register("order-items", OrderItemViewset, basename='order-items')
router.register("categories", CategoriesViewSet, basename='categories')
router.register("lecturers", LecturersViewset, basename='lecturers')
router.register('blogposts', PostViewset, basename='blogposts')
router.register("payments/subscriptions",
                CreateSubscriptionViewset,
                basename="create-subscription")

urlpatterns = [
    path("payments/",
         view=PaymentCreateView.as_view(),
         name="payment-create-view"),
    path("checkout-wh/",
         YandexWebhook.as_view(),
         name="yandex-checkout-webhook"),
    path("cloudpayments-wh/",
         CloudpaymentsWebhook.as_view(),
         name="cloudpayments-webhook"),
]

app_name = "api"
urlpatterns += router.urls
