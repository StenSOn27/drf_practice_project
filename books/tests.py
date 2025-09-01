from django.test import TestCase
from .models import Book, Cover

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
