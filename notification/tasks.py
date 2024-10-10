from celery import shared_task
from datetime import datetime, timedelta

from borrowing.models import Borrowing
from .utils import send_telegram_message


@shared_task
def check_overdue_borrowings():
    tomorrow = datetime.now() + timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow, actual_return_date=None
    )

    if not overdue_borrowings:
        send_telegram_message("No borrowings overdue today!")
    else:
        for borrowing in overdue_borrowings:
            detailed_info = (
                f"Book: {borrowing.book.title}\n"
                f"User: {borrowing.user.username}\n"
                f"Expected Return Date: {borrowing.expected_return_date}"
            )

            send_telegram_message(detailed_info)
