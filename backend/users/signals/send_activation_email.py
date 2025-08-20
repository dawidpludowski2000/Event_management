from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser, ActivationToken

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    if not created:
        return  # tylko przy nowym użytkowniku

    # Dezaktywacja konta
    instance.is_active = False
    instance.save(update_fields=["is_active"])

    # Tworzenie tokena
    token_obj = ActivationToken.objects.create(user=instance)

    # Link aktywacyjny
    activation_link = f"http://localhost:8000/api/users/activate/{token_obj.token}/"

    # Wysyłka maila
    send_mail(
        subject="Aktywuj swoje konto",
        message=f"Cześć! Aktywuj swoje konto klikając w poniższy link:\n{activation_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.email],
        fail_silently=False,
    )

    print(f"[SIGNAL] Mail aktywacyjny wysłany do {instance.email}")
