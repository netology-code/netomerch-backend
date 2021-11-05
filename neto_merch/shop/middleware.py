from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from rest_framework.request import Request
from rest_framework import status
from .views import ProductViewSet, CategoryViewSet
from django.core.cache import cache
from django.conf import settings


class CacheMethodsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.path = request.path_info.lstrip('/').split('/')[2]
        if self.path == 'categories':
            categories = cache.get('category')
            print(categories)
            return JsonResponse(categories, status=status.HTTP_200_OK)
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        if self.path == 'categories':
            if 'category' in cache:
                categories = cache.get('category')
                print(categories)
                return JsonResponse(categories, status=status.HTTP_200_OK)
            # else:
            # TODO: тут надо как-то вызвать нашу функцию Get из класса CategoryViewSet, но как это сделать - я хз
            # TODO: был вариант сделать Redirect, но он не сильно помогает, т.к. не знает такого пути
            # TODO: Прямой вызов тоже не помогает. Если решить этот вопрос - все заработает

        elif self.path == 'items':
            if 'items' in cache:
                products = cache.get('items')
                return JsonResponse(products, status=status.HTTP_200_OK)

            # else:
                # TODO: Аналогично If, который выше
        else:
            return None