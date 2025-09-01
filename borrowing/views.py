import datetime
from rest_framework import viewsets, generics, status
from .models import Borrowing
from .serializers import BorrowingCreateSerializer, BorrowingReadSerializer, BorrowingReturnSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=['post'], serializer_class=BorrowingReturnSerializer)
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        serializer = self.get_serializer(instance=borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)

        if borrowing.actual_return_date is not None:
            return Response(
                {"error": "Book already returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = datetime.datetime.now(datetime.timezone.utc)
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response(
            {
                "message": "Book succesfully returned.",
                "return_date": borrowing.actual_return_date,
                "book": book.title,
                "updated_inventory": book.inventory
            },
            status=status.HTTP_200_OK
        )



class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]
