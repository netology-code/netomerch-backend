from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from config.api_docs import urlpatterns as api_docs_urlpatterns

urlpatterns = api_docs_urlpatterns + [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.products.urls")),
    path("mail/", include("apps.orders.urls")),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
