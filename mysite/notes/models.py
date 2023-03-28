from django.db import models


class Note(models.Model):
    text = models.TextField(max_length=255)
    is_done = models.BooleanField(help_text='temp text')
    time = models.TimeField()
    priority = models.IntegerField()

    class Meta:
        verbose_name = "1"
        verbose_name_plural = "Заметки"

    def __str__(self):
        return f"заметка с id{self.id}"
