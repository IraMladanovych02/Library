from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


class BorrowingListView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)

        if user.is_superuser:
            queryset = Borrowing.objects.all()

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            if is_active is not None:
                is_active = bool(is_active and is_active.lower() == "true")
                queryset = queryset.filter(is_active=is_active)

        else:
            queryset = Borrowing.objects.filter(user_id=user.id)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user_id=user.id)

        return queryset.filter(id=self.kwargs["pk"])


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
