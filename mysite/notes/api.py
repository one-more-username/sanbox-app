from django.http import HttpResponse
from rest_framework import generics, viewsets

from .models import Note
from .serializers import NoteSerializer


# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
