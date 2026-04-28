from django.contrib.auth.models import User
from django.db import models

from offers_app.models import OfferDetail


class Order(models.Model):
    """Eine Bestellung eines Customers bei einem Business-User."""

    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_as_customer'
    )
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_as_business'
    )
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=IN_PROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} – {self.status}'