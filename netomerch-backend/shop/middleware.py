from django.http import HttpResponse
from rest_framework import status
from django.core.cache import cache
import json


class CacheMethodsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.path = request.path_info.lstrip('/').split('/')[2]
        if self.path in cache:
            if cache.get(self.path) is not None:
                resp = json.loads(cache.get(self.path))
                return HttpResponse(resp, status=status.HTTP_200_OK)
        else:
            response = self.get_response(request)
            print(json.dumps(response.data))
            cache.set(self.path, json.dumps(response.data))
            return response