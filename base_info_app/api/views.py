from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from profiles_app.models import UserProfile
from reviews_app.models import Review


class BaseInfoView(APIView):
    """Returns public platform statistics."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(self._get_base_info())

    def _get_base_info(self):
        return {
            "review_count": self._get_review_count(),
            "average_rating": self._get_average_rating(),
            "business_profile_count": self._get_business_count(),
            "offer_count": self._get_offer_count(),
        }

    def _get_review_count(self):
        return Review.objects.count()

    def _get_average_rating(self):
        average = Review.objects.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        return round(average, 1) if average else 0

    def _get_business_count(self):
        return UserProfile.objects.filter(type=UserProfile.BUSINESS).count()

    def _get_offer_count(self):
        return Offer.objects.count()