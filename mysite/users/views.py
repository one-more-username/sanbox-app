from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
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

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     #
    #     profile = Profile.objects.get(user=request.data['id'])
    #     # print("VALUES", request.data)
    #     #
    #     return Response((serializer.data, profile), status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     data = self.request.data
    #
    #     if "id" not in data:
    #         raise ValidationError({
    #             "id": "Profile with this id doesn't exist",
    #         })
    #
    #     try:
    #         profile = Profile.objects.get(user=data["id"])
    #     except Profile.DoesNotExist:
    #         return Response(
    #             'No profile with the id ({0}) found'.format(id),
    #             status=status.HTTP_404_NOT_FOUND
    #         )

        # device = serializer.save()

        # profile.devices.add(device)


class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.PasswordSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
