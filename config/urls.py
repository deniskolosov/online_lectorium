from allauth.account.views import PasswordResetFromKeyView
from allauth.account import urls
from djoser import urls
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from django.urls import include, path, re_path
from rest_auth.views import (PasswordChangeView, PasswordResetConfirmView,
                             PasswordResetView)


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path("",
         TemplateView.as_view(template_name="pages/home.html"),
         name="home"),
    # # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # # User management
    path("users/", include("afi_backend.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("payments/", include("afi_backend.payments.urls",
                              namespace="payments")),
    path("robots.txt", robots_txt),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('favicon.ico',
             RedirectView.as_view(url='images/favicons/favicon.ico'))
    ]

schema_view = get_schema_view(
    openapi.Info(
        title="Art For Introvert backend API",
        default_version='v1',
        description="Art For Introvert API docs",
        contact=openapi.Contact(email="developer@artforintrovert.ru"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny, ),
)


# API URLS
class MyTokenObtainPairView(TokenObtainPairView):
    queryset = ''


class MyTokenRefreshView(TokenRefreshView):
    queryset = ''


from rest_auth import urls

urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path('api/auth-token/',
         MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/auth-token/refresh/',
         MyTokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/password-change/',
         PasswordChangeView.as_view(queryset=''),
         name='password-change'),
]

# SWAGGER URLS
urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))
                       ] + urlpatterns
