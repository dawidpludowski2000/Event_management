from rest_framework.response import Response

def success(message="OK", data=None, status=200):
    return Response({
        "success": True,
        "message": message,
        "data": data,
    }, status=status)

def error(message="Błąd", errors=None, status=400):
    return Response({
        "success": False,
        "message": message,
        "errors": errors or {},
    }, status=status)
