from django.urls import path

from apps.orders.views import send_email

urlpatterns = [
    path('', send_email)
]
