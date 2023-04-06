from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime

User = get_user_model()


class Note(models.Model):
    text = models.TextField(max_length=255)
    is_done = models.BooleanField(help_text='temp text', default=False)
    time = models.TimeField(null=True, blank=True)
    # datetime = models.TimeField(default=datetime.)
    priority = models.IntegerField()
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, null=True)
    done_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "All notes"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"Note with id{self.id}"
