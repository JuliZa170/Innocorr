# middleware.py

import json
from django.http import JsonResponse

class JSONResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code >= 400:
            # Si la respuesta tiene un código de estado de error (400 o más),
            # generamos una respuesta JSON personalizada con el mensaje de error.
            response = JsonResponse(
                {
                    'error': {
                        'status_code': response.status_code,
                        'message': response.reason_phrase,
                    }
                },
                status=response.status_code
            )

        return response
