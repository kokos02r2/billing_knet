import base64
import os
from functools import wraps

from django.http import HttpResponse
from dotenv import load_dotenv

load_dotenv()

login = os.getenv('SBERBANK_LOGIN')
password = os.getenv('SBERBANK_PASSWORD')


def basic_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return HttpResponse('Unauthorized', status=401)

        auth_type, credentials = auth_header.split()
        if auth_type.lower() != 'basic':
            return HttpResponse('Unauthorized', status=401)

        username, password = base64.b64decode(credentials).decode('utf-8').split(':')

        if username != login or password != password:
            return HttpResponse('Unauthorized', status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
