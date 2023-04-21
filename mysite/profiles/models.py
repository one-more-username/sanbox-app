from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# Create your models here.

#   use post_save for create User and Profile at the one moment
#   https://dev-gang.ru/article/signaly-v-django-v2xrwoluji/

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

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, primary_key=True)
    # owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, null=True)
    birthdate = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=1, blank=True, choices=Gender.choices)  # default=Null or null=True
    image = models.ImageField(upload_to=upload_path_autor, blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        # return f"Profile {self.user.first_name} {self.user.last_name}"
        return f"Profile with id{self.user.id}"


# triggered when User object is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )
