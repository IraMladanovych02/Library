from django.urls import path

from book.views import BookListView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path("books/<int:pk>", BookDetailView.as_view(), name='book_detail'),
]

app_name = 'book'
