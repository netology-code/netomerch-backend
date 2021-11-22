from django.http.response import JsonResponse
from celery.result import AsyncResult


def get_task_status(request, task_id):
    task = AsyncResult(task_id)
    result = {
        'id': task.id,
        'status': task.status,
        'result': str(task.result)
    }
    return JsonResponse(result, safe=False)
