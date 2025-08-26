from rest_framework import serializers

from .models import Book, Cover


class BookSerializer(serializers.ModelSerializer):
    cover = serializers.ChoiceField(choices=[(cover.value, cover.value) for cover in Cover])
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee"
        ]


class BookListSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]


class BookDetailSerializer(BookSerializer):
    pass
