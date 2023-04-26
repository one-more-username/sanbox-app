from django.db import transaction
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

    # @extend_schema() for change structure of response in UserCreateView??
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        user.save()

        profile = Profile(
            user=user,
            gender=serializer.validated_data['profile']['gender'],
            birthdate=serializer.validated_data['profile']['birthdate']
        )
        profile.save()
        user.refresh_from_db()
        sr_user = serializers.UserSerializer(user)

        return Response(sr_user.data, status=status.HTTP_201_CREATED)


class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.PasswordSerializer

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
