from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extends the Django user model with profile information."""

    CUSTOMER = 'customer'
    BUSINESS = 'business'
    TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (BUSINESS, 'Business'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} ({self.type})'