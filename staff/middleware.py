from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings

from django.shortcuts import redirect
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class StaffAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url_name = resolve(request.path_info).url_name

        # Exclude the login page from the check
        if current_url_name != 'staff_login' and not request.session.get('staff_id'):
            return redirect('staff_login')

        response = self.get_response(request)
        return response