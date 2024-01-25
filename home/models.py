import uuid

from django.db import models

from helpers.models import TrackingModel
from users.models import User


class Notification(models.Model):
    context = models.TextField(blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
