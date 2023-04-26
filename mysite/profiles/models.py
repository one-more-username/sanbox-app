from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# Create your models here.

# Profile
#   photo/avatar(downloaded). url for download file
def upload_path_autor(instance, filename):
    return 'profile_images/{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, primary_key=True)
    birthdate = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=1, blank=True, choices=Gender.choices)  # default=Null or null=True
    image = models.ImageField(upload_to=upload_path_autor, blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return f"Profile with id{self.user.id}"

