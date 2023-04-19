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
def upload_path_autor(instance, filename):
    return 'profile_images/{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthdate = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=1, blank=True, choices=Gender.choices)
    image = models.ImageField(upload_to=upload_path_autor, blank=True, null=True)
    # image = models.ImageField(upload_to="images/", blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return f"Profile {self.user.first_name} {self.user.last_name}"


class ProfilePhoto(models.Model):
    images = models.ImageField(upload_to=upload_path_autor, blank=True, null=True)
    # images = models.ImageField(upload_to="images/", blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ProfilePhotos')
