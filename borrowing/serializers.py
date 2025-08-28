from datetime import date
from rest_framework import serializers
from .models import Borrowing
from books.serializers import BookSerializer


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        ]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["id", "expected_return_date", "book"]

    def validate_book(self, book):
        if book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock")
        return book

    def validate_expected_return_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("Return date must be in the future")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        book = validated_data["book"]

        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(
            user=request.user,
            **validated_data
        )
        return borrowing
