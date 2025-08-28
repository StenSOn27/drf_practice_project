from django.urls import include, path
from rest_framework.routers import DefaultRouter
from borrowing.views import BorrowingViewSet, BorrowingCreateView

app_name = "borrowings"

router = DefaultRouter()
router.register("", BorrowingViewSet, basename="borrowings")

urlpatterns = [
    path("create/", BorrowingCreateView.as_view(), name="borrowing-create"),
    path("", include(router.urls)),
]