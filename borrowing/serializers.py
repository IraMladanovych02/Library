from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        ]

    def create(self, validated_data):
        book_id = validated_data["book_id"]
        user_id = self.context["request"].user

        if not user_id.is_authenticated:
            raise serializers.ValidationError(
                "User must be authenticated to borrow a book."
            )

        if book_id.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        borrowing = Borrowing.objects.create(
            borrow_date=validated_data["borrow_date"],
            expected_return_date=validated_data["expected_return_date"],
            actual_return_date=validated_data["actual_return_date"],
            book_id=book_id,
            user_id=user_id,
        )

        book_id.inventory -= 1
        book_id.save()

        return borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
