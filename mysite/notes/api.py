from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Note
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, DoesntDone
from .serializers import NoteSerializer


# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    # permission_classes = (IsAuthenticated, )
    permission_classes = (IsAuthenticatedOrReadOnly, DoesntDone,)

    # TODO setDone, work with auth
    # rewrite actions `list()`, `create()`, `update()`, `destroy()`

    # def get_serializer_class(self):
    #     if self.action in ["retrieve", "list"]:
    #         return self.serializer_class
        # return

    @action(methods=['get', 'post'], detail=True, url_path='done')
    def set_done(self, request, *args, **kwargs):
        note = self.get_object()
        note.is_done = True
        note.save()
        return Response(self.get_serializer(note).data)

    @action(methods=['get', 'post'], detail=False, url_path='doneall')
    def set_all_done(self, request, *args, **kwargs):
        notes = Note.objects.all()

        for note in notes:
            if not note.is_done:
                note.is_done = True

        for doned in notes:
            doned.save()

        # print(doned)      #   wtf   https://stackoverflow.com/questions/6221510/django-calling-save-on-a-queryset-object-queryset-object-has-no-attribute-s

        return Response(self.get_serializer(doned).data)

    @action(methods=['get', 'post'], detail=False, url_path='undoneall')
    def set_all_undone(self, request, *args, **kwargs):
        notes = Note.objects.all()

        for note in notes:
            if note.is_done:
                note.is_done = False

        for undoned in notes:
            undoned.save()

        return Response(self.get_serializer(undoned).data)

    def perform_update(self, serializer):
        serializer.save()

# class NoteAPIList(generics.ListCreateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class NoteAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     permission_classes = (IsOwnerOrReadOnly,)
#
#
# class NoteAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     # permission_classes = (IsAdminUser, )
#     permission_classes = (IsAdminOrReadOnly,)
#
#
# class NoteAPISetDone(generics.GenericAPIView):
#     queryset = Note.objects.all()
#     permission_classes = (DoesntDone,)
#     lookup_field = "id"
#
#     def get(self, request, *args, **kwargs):
#         # note = self.get_queryset().get(id=id)
#         # print('serializer_class', self.serializer_class)
#         note = self.get_object()
#         note.is_done = True
#         note.save()
#         return Response()
