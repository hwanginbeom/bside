from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

schema_url_patterns = [ path('', include('post.urls')), ]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="59 API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rydn2004@naver.com")

    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('post.urls')),
    path('api-jwt-auth/', obtain_jwt_token),
    path('api-jwt-auth/refresh/', refresh_jwt_token),
    path('api-jwt-auth/verify/', verify_jwt_token),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
