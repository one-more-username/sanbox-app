from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # first_name = models.CharField(max_length=30, default=User.get_short_name)
    # last_name = models.CharField(max_length=30, default=User.first_name)
    birthdate = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=1, blank=True, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
    ))
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "profile verbose"
        verbose_name_plural = "profile plural"

    def __str__(self):
        return f"Profile {self.user.first_name} {self.user.lasr_name}"
