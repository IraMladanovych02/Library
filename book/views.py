from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics

from book.models import Book
from book.serializers import BookSerializer


class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")
        queryset = Book.objects.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Filter by book title (ex. ?title=Harry)"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
