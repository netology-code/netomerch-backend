from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

openapi_info = openapi.Info(
        title="Nemerch API",
        default_version='v1',
        description="Backend for nemerch online shop",
    )
schema_view = get_schema_view(
    openapi_info,
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
