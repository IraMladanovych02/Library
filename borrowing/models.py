from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowing")
    user_id = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name="borrowings")

    def clean(self):
        if self.expected_return_date:
            if self.borrow_date > self.expected_return_date:
                raise ValidationError(
                    "Expected return date should be after the borrow date."
                )

            if (self.actual_return_date
                    and self.actual_return_date > self.expected_return_date):
                raise ValidationError(
                    "Actual return date should not be after the expected return date."
                )

        if self.actual_return_date:
            if self.actual_return_date < self.borrow_date:
                raise ValidationError(
                    "Actual return date should not be before the borrow date."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Borrowed book {self.book_id} by user {self.user_id}"
