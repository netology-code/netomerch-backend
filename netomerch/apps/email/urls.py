from django.urls import path

from apps.email.views import callback

urlpatterns = [
    path('', callback)
]
