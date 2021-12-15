from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.api_docs import urlpatterns as api_docs_urlpatterns

APIV1 = "api/v1/"

urlpatterns = api_docs_urlpatterns + [
    path("admin/", admin.site.urls),
    path(APIV1, include("apps.products.urls")),
    path(APIV1, include("apps.orders.urls")),
    path(APIV1, include("apps.reviews.urls")),
    path(f"{APIV1}task/", include("apps.taskqueue.urls")),
    path(f"{APIV1}callback/", include("apps.email.urls")),
    path('summernote/', include('django_summernote.urls')),
    path(APIV1, include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
