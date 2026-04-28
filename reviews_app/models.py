from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    """Bewertung eines Business-Users durch einen Customer."""

    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    rating = models.IntegerField()  # 1–5
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        return f'Review by {self.reviewer.username} for {self.business_user.username}'