from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review
from .permissions import IsCustomerUser, IsReviewCreator
from .serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    """Lists reviews or creates a new review."""

    serializer_class = ReviewSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["updated_at", "created_at", "rating"]
    ordering = ["-updated_at"]
    pagination_class = None

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.all()
        queryset = self._filter_by_business_user(queryset)
        queryset = self._filter_by_reviewer(queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def _filter_by_business_user(self, queryset):
        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            return queryset.filter(business_user__id=business_user_id)
        return queryset

    def _filter_by_reviewer(self, queryset):
        reviewer_id = self.request.query_params.get("reviewer_id")
        if reviewer_id:
            return queryset.filter(reviewer__id=reviewer_id)
        return queryset


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """Updates or deletes own reviews."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewCreator]
    queryset = Review.objects.all()
    http_method_names = ["patch", "delete"]