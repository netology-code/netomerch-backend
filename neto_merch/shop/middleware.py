from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from .views import ProductViewSet, CategoryViewSet
from django.core.cache import cache


class CacheGetMethods:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def cache_get(self, request, view_func, view_args, view_kwargs):
        if request.path == 'api/v1/categories':
            if 'categories' in cache:
                categories = cache.get('categories')
                return JsonResponse(categories, status=status.HTTP_200_OK)

            else:
                req = Request(request)
                res = CategoryViewSet.retrieve(req)
                cache.set('categories', res.data)
                return JsonResponse(res.data, status=res.status_code)

        elif request.path == 'api/v1/products':
            if 'products' in cache:
                products = cache.get('products')
                return JsonResponse(products, status=status.HTTP_200_OK)

            else:
                req = Request(request)
                res = ProductViewSet.retrieve(req)
                cache.set('products', res.data)
                return JsonResponse(res.data, status=res.status_code)
        else:
            return None