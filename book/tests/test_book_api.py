from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from book.models import Book
from book.serializers import BookSerializer

BOOK_URL = reverse("book:book-list")


def detail_url(book_id):
    return reverse("book:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "testtitle",
        "author": "testauthor",
        "cover": "HARD",
        "inventory": 10,
        "daily_fee": 11.99,
    }
    defaults.update(**params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = sample_book()
        self.url = detail_url(self.book.id)

    def test_list_books(self):
        response = self.client.get(BOOK_URL)

        books = Book.objects.order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_book(self):
        response = self.client.get(self.url)
        serializer = BookSerializer(self.book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_title(self):
        book1 = sample_book(title="testtitleforsure")
        book2 = sample_book(title="exactlytesttitle")
        serializer1 = BookSerializer(book1)
        serializer2 = BookSerializer(book2)
        response = self.client.get(BOOK_URL, {"title": f"{book1.title}"})
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_create_forbidden(self):
        payload = {
            "title": "testtitle",
            "author": "testauthor",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_forbidden(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10.00,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_forbidden(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_forbidden(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@testmail.com", "testpassword"
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()
        self.url = detail_url(self.book.id)

    def test_list_books(self):
        response = self.client.get(BOOK_URL)
        books = Book.objects.order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_title(self):
        book1 = sample_book(title="Kobzar")
        book2 = sample_book(title="Harry Poter")
        serializer1 = BookSerializer(book1)
        serializer2 = BookSerializer(book2)
        response = self.client.get(BOOK_URL, {"title": f"{book1.title}"})
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_detail_book(self):
        response = self.client.get(self.url)
        serializer = BookSerializer(self.book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_forbidden(self):
        payload = {
            "title": "testtitle",
            "author": "testauthor",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_forbidden(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10.00,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_forbidden(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_forbidden(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@testmail.com", "testpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()
        self.url = detail_url(self.book.id)

    def test_create_book(self):
        payload = {
            "title": "testtitle",
            "author": "testauthor",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_put_book(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10.00,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.book, key))

    def test_patch_book(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.book, key))

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
