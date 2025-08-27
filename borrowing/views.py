from rest_framework import viewsets
from .models import Borrowing
from .serializers import BorrowingReadSerializer


class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.select_related('book', 'user').all()
    serializer_class = BorrowingReadSerializer
