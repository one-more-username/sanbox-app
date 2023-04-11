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
    location = models.CharField(max_length=1, blank=True, choices=(
        ('H', 'Home'),
        ('W', 'Work'),
    ))
    # in serializer filter subnotes by Notes?

    class Meta:
        verbose_name = "note"
        verbose_name_plural = "note"

    def __str__(self):
        return f"Note with id{self.id}"


class SubNote(models.Model):
    is_done = models.BooleanField()
    text = models.TextField()
    from_note = models.ForeignKey(
        Note, verbose_name='From note', on_delete=models.CASCADE, related_name='subnotes',
    )

    class Meta:
        verbose_name = "subnote"

    def __str__(self):
        return f"Subnote with id:{self.id}"
