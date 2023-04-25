from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from profiles.models import Profile
from users import serializers
from django.contrib.auth.models import User


# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #
        @receiver(post_save, sender=User)
        def create_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)

        user = User.objects.get(id=serializer.data['id'])

        data = {
            "created user": serializer.data,
            "created profile with id": user.profile.user_id
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.PasswordSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
