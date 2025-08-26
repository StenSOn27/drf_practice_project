from rest_framework import viewsets

from books.models import Book
from .serializers import (
    BookDetailSerializer, BookListSerializer
) 

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """ 
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer
