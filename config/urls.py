from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title = "SERGINNETTI REST API",
        default_version="v0",
        description="THIS IS A WOMEN`S CLOTHES ONLINE SHOP",
        contact=openapi.Contact("")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('discount/', include('discount.urls')),
    path('main/', include('main.urls')),

    path('swagger/', schema_view.with_ui('swagger',cache_timeout=0),name='swagger-docs'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)