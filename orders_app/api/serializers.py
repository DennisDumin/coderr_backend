from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializes an order with all snapshot data."""

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "offer_detail",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """Creates an order from an offer detail ID."""

    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Offer detail not found.")
        return value

    def create(self, validated_data):
        detail = OfferDetail.objects.get(pk=validated_data["offer_detail_id"])
        customer = self.context["request"].user
        business = detail.offer.creator

        return Order.objects.create(
            customer_user=customer,
            business_user=business,
            offer_detail=detail,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status=Order.IN_PROGRESS,
        )


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Updates only the order status."""

    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        allowed_statuses = [
            Order.IN_PROGRESS,
            Order.COMPLETED,
            Order.CANCELLED,
        ]

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Status must be one of {allowed_statuses}."
            )

        return value