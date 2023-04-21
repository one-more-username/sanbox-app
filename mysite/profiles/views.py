from django.shortcuts import render, redirect
from rest_framework import generics

# from django.http import HttpResponseRedirect

from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.

#   APIView, genericAPIView
# class UserRegistrationView(generics.CreateAPIView): #   ListCreateAPIView?
#     # queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(user=user)

class UpdateProfileView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DetailProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

