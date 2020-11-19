from django.urls import path

from afi_backend.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from afi_backend.users.api.views import ActivateUser

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("activate-user/", ActivateUser.as_view(), name="activate-user"),
]
