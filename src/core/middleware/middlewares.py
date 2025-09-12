# middlewares.py
from django.http import JsonResponse
from django.utils.timezone import now

from .exceptions import BusinessValidationError


class BusinessErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except BusinessValidationError as e:
            return JsonResponse({
                "status": "error",
                "message": e.mensagem,
                "code": e.codigo,
                "timestamp": now().isoformat()
            }, status=e.codigo)
        except ValueError as e:
            return JsonResponse({
                "status": "error",
                "message": str(e),
                "code": 400,
                "timestamp": now().isoformat()
            }, status=400)
