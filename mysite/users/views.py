from rest_framework import generics, status
from rest_framework.response import Response

from users import serializers
from django.contrib.auth.models import User

from users.utils import removekey


# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #
        # data = removekey(serializer.data, 'password')
        #

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.PasswordSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


