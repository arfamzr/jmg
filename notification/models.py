from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User


class Notification(models.Model):
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(_("message"), max_length=255)
    link = models.CharField(_("link"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.to_user} - {self.pk}'
