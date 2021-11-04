from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from views import CategoryViewSet, ProductViewSet
from django.core.cache import cache
from django.conf import settings



class CacheGetMethods:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def cache_get(self, request, view_func, view_args, view_kwargs):
        if request.path == 'api/v1/categories':
            if 'product' in cache:
                products = cache.get('product')
                return JsonResponse(products, status=status.HTTP_200_OK)

            else:

            # Django and DRF have different Request
            # convert django.core.handlers.wsgi.WSGIRequest to rest_framework.request.Request
            req = Request(request)
            res = HogeView.get(HogeView, req)

            # process_view must return django.http.Response
            # DRF's view returns rest_framework.response.Response
            # convert rest_framework.response.Response to django.http.Response
            return JsonResponse(res.data, status=res.status_code)
        else:
            return None

def cache_get_methods(get_response):
    def middleware(request):

        response = get_response(request)
        t2 = time.time()
        print("TOTAL TIME:", (t2 - t1))
        return response
    return middleware