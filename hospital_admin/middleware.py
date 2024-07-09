class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = "no-store, no-cache, must-revalidate, proxy-revalidate"
        response['Pragma'] = "no-cache"
        response['Expires'] = "0"
        response['Surrogate-Control'] = "no-store"
        return response