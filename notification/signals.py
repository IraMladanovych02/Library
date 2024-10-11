from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowing.models import Borrowing
from notification.utils import send_telegram_message



@receiver(post_save, sender=Borrowing)
def order_created(sender, instance, created, **kwargs):
    if created:
        message = f"New order created:\nBook: {instance.book_id}\nUser: {instance.user_id}"
        send_telegram_message(message)
