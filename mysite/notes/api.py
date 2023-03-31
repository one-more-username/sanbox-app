from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Note
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, DoesntDone
from .serializers import NoteSerializer


# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DoesntDone,)
    separator = ','

    # TODO action with params for filtration. Params in body of request. New serializer for this action(for body)

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned articles to given regions,
    #     by filtering against a `regions` query parameter in the URL.
    #     """
    #     notes = self.request.query_params.get("is_done", None)
    #     if notes:
    #          qs = Note.objects.filter()
    #          for note in notes.split(self.separator):
    #              qs = qs.filter(notes__code=note)
    #          return qs
    #
    #     return super().get_queryset()

    @action(methods=['get'], detail=False, url_path='owner')
    def filter_by_owner(self, request, *args, **kwargs):
        owner = request.user.id

        # print(self.request.user)
        # print(request.user.id)

        notes = Note.objects.filter(owner=owner)

        return Response(self.get_serializer(notes, many=True).data)

    # @action(methods=['get'], detail=False, url_path='filtered')
    # def filter_by_params(self, request, *args, **kwargs):
    #     owner = request.user.id
    #
    #     # print(self.request.user)
    #     # print(request.user.id)
    #
    #     notes = Note.objects.filter(owner=owner)
    #
    #     return Response(self.get_serializer(notes, many=True).data)

    @action(methods=['post'], detail=True, url_path='done')
    def set_done(self, request, *args, **kwargs):
        note = self.get_object()
        note.is_done = True
        note.save()
        return Response(self.get_serializer(note).data)

    @action(methods=['post'], detail=False, url_path='doneall')
    def set_all_done(self, request, *args, **kwargs):
        Note.objects.filter(is_done=False).update(is_done=True)

        notes = Note.objects.all()

        return Response(self.get_serializer(notes, many=True).data)

    @action(methods=['post'], detail=False, url_path='undoneall')
    def set_all_undone(self, request, *args, **kwargs):
        Note.objects.filter(is_done=True).update(is_done=False)

        notes = Note.objects.all()

        return Response(self.get_serializer(notes, many=True).data)

    # def perform_update(self, serializer):
    #     serializer.save()
