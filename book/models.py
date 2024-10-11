from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "Hard"),
        ("SOFT", "Soft")
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    inventory = models.PositiveIntegerField()
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
