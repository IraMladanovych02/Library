from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book
from borrowing.models import Borrowing


BORROWING_URL = reverse("borrowing:borrowing-list")


def sample_borrowing(**params):
    user = get_user_model().objects.create_user(
        email="active@test.com",
        password="testpass",
    )
    book = Book.objects.create(
        title="Active Book",
        author="Active Author",
        inventory=1,
        daily_fee=10.00,
    )
    defaults = {
        "user_id": user,
        "book_id": book,
        "expected_return_date": datetime.now().date() + timedelta(days=3),
        "borrow_date": datetime.now().date(),
    }
    defaults.update(params)
    return Borrowing.objects.create(**defaults)


class BorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com", password="testpassword"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=1,
            daily_fee=10.00,
        )
        self.url = reverse("borrowing:borrowing-list")
        self.client.force_authenticate(user=self.user)

    def test_create_borrowing(self):
        with patch("asyncio.run") as redirect_mock:
            redirect_mock.return_value = None

            data = {
                "borrow_date": datetime.now().date(),
                "expected_return_date": datetime.now().date() + timedelta(days=3),
                "book": self.book.pk,
            }

            response = self.client.post(self.url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            self.assertEqual(Borrowing.objects.count(), 0)

    def test_borrow_nonexistent_book(self):
        data = {"book": 999, "expected_return_date": "2023-11-01"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Borrowing.objects.count(), 0)

    def test_borrow_unavailable_book(self):
        self.book.inventory = 0
        self.book.save()

        data = {"book": self.book.id, "expected_return_date": "2023-11-01"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Borrowing.objects.count(), 0)

    def test_list_borrowings_by_user(self):
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url, {"user_id": self.user.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 0
        )

    def test_list_all_borrowings_as_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.client.force_authenticate(user=superuser)

        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_borrowings_by_title(self):
        borrowing = sample_borrowing(user_id=self.user, book_id=self.book)

        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url, {"title": self.book.title}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], borrowing.id)

