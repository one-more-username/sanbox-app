from rest_framework import generics


from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.

class UpdateProfileView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DetailProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

