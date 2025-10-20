from django.http import JsonResponse
from rest_framework.response import Response

def success(message="OK", data=None, status=200):
    return Response({
        "success": True,
        "message": message,
        "data": data,
    }, status=status)

def error(message="Error", errors=None, status=400):
    return JsonResponse({
        "success": False,
        "message": message,
        "detail": message,  
        "errors": errors or {}
    }, status=status)

