from django.test import TestCase
from django.urls import reverse
from datetime import timedelta, date

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authentication import get_user_model

from books.models import Book, Cover
from borrowing.models import Borrowing


User = get_user_model()


class BorrowingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover=Cover.HARD.value,
            inventory=3,
            daily_fee="1.50",
        )

    def test_create_borrowing(self):
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=date.today() + timedelta(days=5),
        )
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(str(borrowing), f"{self.user.email} → {self.book.title}")
        self.assertIsNone(borrowing.actual_return_date)
        self.assertTrue(borrowing.expected_return_date > borrowing.borrow_date)


class BorrowingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.staff = User.objects.create_user(
            email="staff@example.com", password="password123", is_staff=True
        )
        self.book = Book.objects.create(
            title="Borrowed Book",
            author="Author",
            cover=Cover.HARD.value,
            inventory=2,
            daily_fee="2.00",
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=date.today() + timedelta(days=3),
        )

    def test_list_borrowings_user_only_sees_own(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.email)

    def test_list_borrowings_staff_sees_all(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse("borrowings:borrowings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_borrowing(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowing-create")
        data = {
            "book": self.book.id,
            "expected_return_date": (date.today() + timedelta(days=7)).isoformat(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 1)

    def test_return_book_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowings-return-book", args=[self.borrowing.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 3)

    def test_return_book_twice_fails(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowings-return-book", args=[self.borrowing.id])
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
