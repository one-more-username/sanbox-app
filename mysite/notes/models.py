from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# new app with model for Profile
# Profile
#   birthdate
#   male/female
#   photo/avatar(downloaded). url for download file
#
# get_user_model.User
#   name
#   surname
#   birthdate
#   male/female
#
#   * in Note infinite quantity of photo
#


class Note(models.Model):
    class Location(models.TextChoices):
        HOME = 'H', 'Home'
        WORK = 'W', 'Work'

    text = models.TextField(max_length=255)
    is_done = models.BooleanField(help_text='temp text', default=False)
    time = models.TimeField(null=True, blank=True)
    priority = models.IntegerField()
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, null=True)
    done_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=1, blank=True, choices=Location.choices)
    # location = models.CharField(max_length=1, blank=True, choices=(
    #     ('H', 'Home'),
    #     ('W', 'Work'),
    # ))

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
    estimated_time = models.IntegerField(null=True, blank=True)
    spent_time = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "subnote"
        constraints = [
            models.CheckConstraint(
                # name="spent_time_only_for_doned",
                name="%(class)s_spent_time_error",
                check=(
                    models.Q(
                        is_done=True,
                        spent_time__isnull=False
                    )
                    | models.Q(
                        is_done=False,
                        spent_time__isnull=True,
                    )
                ),
                violation_error_message="Can't be done without spent_time"
            ),
        ]

    def __str__(self):
        return f"Subnote with id:{self.id}"
