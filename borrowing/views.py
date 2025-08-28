from rest_framework import viewsets, generics
from .models import Borrowing
from .serializers import BorrowingCreateSerializer, BorrowingReadSerializer
from rest_framework.permissions import IsAuthenticated

class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorrowingReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.select_related('book', 'user').all()

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            is_active_bool = is_active.lower() in ["true", "1"]
            queryset = queryset.filter(actual_return_date__isnull=is_active_bool)

        if user.is_staff:
            user_id_param = self.request.query_params.get("user_id")
            if user_id_param:
                try:
                    user_id = int(user_id_param)
                    queryset = queryset.filter(user_id=user_id)
                except ValueError:
                    pass

        return queryset


class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]
