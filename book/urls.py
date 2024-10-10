from django.urls import path

from book.views import BookListView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path("books/<int:pk>", BookDetailView.as_view(), name='book-detail'),
]

app_name = 'book'
