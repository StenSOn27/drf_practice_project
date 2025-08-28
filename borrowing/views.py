from rest_framework import viewsets, generics
from .models import Borrowing
from .serializers import BorrowingCreateSerializer, BorrowingReadSerializer


class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.select_related('book', 'user').all()
    serializer_class = BorrowingReadSerializer


class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
