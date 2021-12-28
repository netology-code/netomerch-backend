from django.urls import path

from apps.taskqueue.views import get_task_status

urlpatterns = [
    path('<str:task_id>', get_task_status)
]
