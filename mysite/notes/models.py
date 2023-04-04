from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Note(models.Model):
    text = models.TextField(max_length=255)
    is_done = models.BooleanField(help_text='temp text', default=False)
    time = models.TimeField(default=timezone.now)
    priority = models.IntegerField()
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, null=True)

    # add new field 'done_at'       # when it`s done

    class Meta:
        verbose_name = "All notes"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"Note with id{self.id}"
