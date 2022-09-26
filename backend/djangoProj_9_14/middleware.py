from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin


class SetToken(MiddlewareMixin):

    def process_response(self, request, response):
        response.set_cookie("csrf_token", get_token(request), expires=60 * 60)
        return response
