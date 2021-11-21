from django.conf.urls import url
from apps.orders.views import send_email


urlpatterns = [
    url('', send_email)
]
