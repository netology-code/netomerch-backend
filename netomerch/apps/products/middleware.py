from django.core.cache import cache


class CacheMethodsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = self.check_method(request)
        if path is False:
            response = self.get_response(request)
            return response

        else:
            return self.set_cache(path, request)

    def check_method(self, requests):
        path = requests.path_info

        if self.check_path(path) is True and requests.method == 'GET':
            if requests.GET.get('search') is None:
                return requests.get_full_path()

            else:
                return False

        else:
            return False

    def check_path(self, path):
        ls_path = path.strip('/').split('/')

        if any(p in ls_path for p in ('categories', 'items')) and 'api' in ls_path:
            return True

        else:
            return False

    def set_cache(self, path, request):
        if cache.get(path) is not None:
            return cache.get(path)

        else:
            response = self.get_response(request)
            if len(response.data.get('results')) != 0:
                cache.set(path, response)
            return response
