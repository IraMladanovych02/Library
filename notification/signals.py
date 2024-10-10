from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowing.models import Borrowing
from .utils import send_telegram_message


@receiver(post_save, sender=Borrowing)
def send_borrowing_create_notification(instance, created, **kwargs):
    if created:
        message = f"New borrowing created: {instance}"
        send_telegram_message(message)
