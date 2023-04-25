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
        headers = self.get_success_headers(serializer.data)

        user = User(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            username=request.data['username'],
            password=request.data['password'],
        )
        # user.save()

        profile = Profile(
            user=user,
            gender=request.data['gender'],
            birthdate=request.data['birthdate']
        )
        # profile.save()

        sr_user = serializers.UserSerializer(data=user)

        if not sr_user.is_valid():
            print("DATA", sr_user.initial_data)

        #   return user & profile instead serializer.data
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)


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
