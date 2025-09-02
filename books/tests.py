from django.test import TestCase
from django.urls import reverse

from books.serializers import BookDetailSerializer, BookListSerializer
from .models import Book, Cover
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authentication import get_user_model


User = get_user_model()

class BookModelTests(TestCase):
    def test_create_book(self):
        book = Book.objects.create(
            title="Test Title",
            author="Test Author",
            cover=Cover.HARD.value,
            inventory=5,
            daily_fee="1.50",
        )
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.cover, "HARD")
        self.assertEqual(book.inventory, 5)
        self.assertEqual(str(book.daily_fee), "1.50")
        self.assertEqual(str(book), "Test Title")


class DefaultUserLibaryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.book = Book.objects.create(
            title="Test Title",
            author="Test Author",
            cover=Cover.HARD.value,
            inventory=5,
            daily_fee="1.50",
        )
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def check_read_only_access(self, instance_id=None):
        list_url = reverse(f"books:book-list")

        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        if instance_id:
            detail_url = reverse(f"books:book-detail", args=[instance_id])

            response = self.client.get(detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.client.put(detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.patch(detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.delete(detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_viewset_access(self):
        self.check_read_only_access(self.book.id)

    def test_book_list_get(self):
        list_url = reverse(f"books:book-list")
        response = self.client.get(list_url)
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_book_detail_get(self):
        detail_url = reverse(f"books:book-detail", args=[self.book.id])
        response = self.client.get(detail_url)
        book = Book.objects.get(id=self.book.id)
        serializer = BookDetailSerializer(book)
        self.assertEqual(response.data, serializer.data)
