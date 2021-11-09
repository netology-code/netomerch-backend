from django.http import HttpResponse
from rest_framework import status
from django.core.cache import cache
import json


class CacheMethodsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # self.path = request.path_info.lstrip('/').split('/')  # TODO: Все, что закомментировано - раскомментировать
        # if 'api' not in self.path or len(self.path) != 4:     # TODO: Как появится API
        #     response = self.get_response(request)
        #     return response
        # else:
        #     self.path = self.path[2]
        #     if self.path in cache.keys('*') and json.loads(cache.get(self.path)) != []:
        #         resp = json.loads(cache.get(self.path))
        #         return HttpResponse(resp, status=status.HTTP_200_OK)
        #
        #     else:
        #         response = self.get_response(request)
        #         if json.dumps(response.data) != []:
        #             cache.set(self.path, json.dumps(response.data))
        #         return response
        response = self.get_response(request)  # TODO: А эти 2 строки
        return response                        # TODO: Надо будет удалить