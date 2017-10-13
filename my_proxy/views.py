import requests
from django.conf import settings
from django.http import HttpResponse
from django.http import QueryDict

from .helpers import replace_words


def proxy_view(request, url, requests_args=None):
    requests_args = (requests_args or {}).copy()
    headers = get_headers(request.META)
    port = request.META['SERVER_PORT']

    params = request.GET.copy()
    url = settings.BASE_PROXY_URL + url
    if 'headers' not in requests_args:
        requests_args['headers'] = {}
    if 'data' not in requests_args:
        requests_args['data'] = request.body
    if 'params' not in requests_args:
        requests_args['params'] = QueryDict('', mutable=True)

    headers.update(requests_args['headers'])
    params.update(requests_args['params'])

    for key in list(headers.keys()):
        if key.lower() == 'content-length':
            del headers[key]

    requests_args['headers'] = headers
    requests_args['params'] = params

    response = requests.request(request.method, url, **requests_args)
    try:
        content = replace_words(response.content.decode(),
                                lambda word: word + '™',
                                lambda word: len(word) == 6,
                                settings.BASE_PROXY_URL,
                                port)

    except UnicodeDecodeError as e:
        content = response.content

    proxy_response = HttpResponse(
        content,
        status=response.status_code)

    excluded_headers = set([
        'connection', 'keep-alive', 'proxy-authenticate',
        'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
        'upgrade',
        'content-encoding',
        'content-length',
    ])
    for key, value in response.headers.items():
        if key.lower() in excluded_headers:
            continue
        proxy_response[key] = value

    return proxy_response


def get_headers(environ):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.  See
    https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
    """
    headers = {}
    for key, value in environ.items():
        # Sometimes, things don't like when you send the requesting host through.
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            headers[key.replace('_', '-')] = value

    return headers
