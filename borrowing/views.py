from rest_framework import viewsets, generics
from .models import Borrowing
from .serializers import BorrowingCreateSerializer, BorrowingReadSerializer
from rest_framework.permissions import IsAuthenticated

class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorrowingReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.select_related('book', 'user').all()
        return Borrowing.objects.select_related('book', 'user').filter(user=user)


class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]
