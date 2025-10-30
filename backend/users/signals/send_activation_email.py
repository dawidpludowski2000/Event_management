import logging
import os


from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models.user import CustomUser
from users.models.activation_token import ActivationToken


@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    if not created:
        return  # tylko przy nowym użytkowniku

    # Dezaktywacja konta
    instance.is_active = False
    instance.save(update_fields=["is_active"])

    # Tworzenie tokena
    token_obj = ActivationToken.objects.create(user=instance)

    activation_link = f"{os.getenv('FRONTEND_ACTIVATION_URL', 'http://localhost:8000')}/api/users/activate/{token_obj.token}/"

    send_mail(
        subject="Aktywacja konta w EventFlow",
        message=(
            f"Cześć {instance.first_name or ''},\n\n"
            f"Dziękujemy za rejestrację w EventFlow!\n"
            f"Aby aktywować swoje konto, kliknij w poniższy link:\n\n"
            f"{activation_link}\n\n"
            f"Pozdrawiamy,\nZespół EventFlow 🚀"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.email],
        fail_silently=False,
    )


    logger = logging.getLogger(__name__)

    logger.info("[SIGNAL] Activation email queued for %s", instance.email)
