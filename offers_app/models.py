from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """Ein Angebot eines Business-Users auf der Plattform."""

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offers'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """Die 3 Pakete (basic, standard, premium) eines Angebots."""

    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'
    OFFER_TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='details'
    )
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)

    class Meta:
        verbose_name = 'Offer Detail'
        verbose_name_plural = 'Offer Details'
        unique_together = ('offer', 'offer_type')

    def __str__(self):
        return f'{self.offer.title} – {self.offer_type}'