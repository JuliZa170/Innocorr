from django.http import JsonResponse

class JSONResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    def process_exception(self, request, exception):
        # Manejar excepciones y devolver una respuesta JSON adecuada
        error_message = str(exception)
        response_data = {'error': error_message}
        return JsonResponse(response_data, status=500)