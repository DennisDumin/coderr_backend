from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializes a single offer detail."""

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "offer_type",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """Serializes offers including their details."""

    details = OfferDetailSerializer(many=True)
    user = serializers.IntegerField(source="creator.id", read_only=True)
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "details",
            "min_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def get_min_price(self, obj):
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices.exists() else None

    def validate_details(self, value):
        required_types = {"basic", "standard", "premium"}
        given_types = {detail["offer_type"] for detail in value}

        if not self.instance and given_types != required_types:
            raise serializers.ValidationError(
                "An offer must contain exactly basic, standard and premium details."
            )

        if self.instance and not given_types.issubset(required_types):
            raise serializers.ValidationError(
                "Details can only use basic, standard or premium as offer_type."
            )

        if len(given_types) != len(value):
            raise serializers.ValidationError(
                "Each offer_type can only be used once."
            )

        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if details_data:
            self._update_details(instance, details_data)

        return instance

    def _update_details(self, instance, details_data):
        for detail_data in details_data:
            offer_type = detail_data.pop("offer_type", None)

            if not offer_type:
                raise serializers.ValidationError(
                    "offer_type is required when updating details."
                )

            OfferDetail.objects.filter(
                offer=instance,
                offer_type=offer_type,
            ).update(**detail_data)