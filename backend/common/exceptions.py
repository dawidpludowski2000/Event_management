from rest_framework.exceptions import ValidationError

def raise_validation(message: str):
    raise ValidationError({"detail": message})
