from rest_framework.response import Response

def ok(data=None, message="OK", status=200):
    return Response({"message": message, "data": data}, status=status)

def fail(message="Request failed", errors=None, status=400):
    return Response({"message": message, "errors": errors}, status=status)
