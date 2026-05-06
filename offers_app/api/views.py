from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from offers_app.models import Offer, OfferDetail
from .permissions import IsBusinessUser, IsOfferCreator
from .serializers import OfferDetailSerializer, OfferSerializer


class OfferPagination(PageNumberPagination):
    """Pagination for offers with configurable page size."""

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferViewSet(ModelViewSet):
    """Handles offer CRUD with filtering, search and ordering."""

    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["min_price", "created_at", "updated_at"]

    def get_queryset(self):
        queryset = Offer.objects.annotate(min_price=Min("details__price"))

        creator_id = self._get_int_query_param("creator_id")
        min_price = self._get_int_query_param("min_price")
        max_delivery_time = self._get_int_query_param("max_delivery_time")

        if creator_id:
            queryset = queryset.filter(creator__id=creator_id)

        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        if max_delivery_time:
            queryset = queryset.filter(
                details__delivery_time_in_days__lte=max_delivery_time
            ).distinct()

        return queryset

    def _get_int_query_param(self, name):
        value = self.request.query_params.get(name)

        if value in [None, ""]:
            return None

        if not value.isdigit():
            raise ValidationError({name: "A valid number is required."})

        return int(value)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action in ["partial_update", "destroy"]:
            return [IsAuthenticated(), IsOfferCreator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class OfferDetailRetrieveView(RetrieveAPIView):
    """Returns a single offer detail."""

    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = OfferDetail.objects.all()