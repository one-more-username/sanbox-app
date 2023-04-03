from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Note
from .permissions import DoesntDone
from .serializers import NoteSerializer, FilterSerializer


# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DoesntDone,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['text']

    # TODO action with params for filtration. Params in body of request. New serializer for this action(for body)
    # __str__ __repr__ __len__ __add__ mustread

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

    # def filter_queryset(self, queryset):

    @action(methods=['post'], detail=False, url_path='filtered')
    def filtered(self, request, *args, **kwargs):
        owner = request.user.id

        serializer_class = FilterSerializer(data=request.data)

        if not serializer_class.is_valid(raise_exception=True):
            print(serializer_class.errors)
        else:
            print('validated data', serializer_class.validated_data)

        # print(serializer_class.is_valid())  # true if exist fields 'is_done', 'time', 'priority'

        notes = Note.objects.filter(owner_id=owner)

        # valid_notes = serializer_class.validated_data

        vd: dict = serializer_class.validated_data    # OrderedDict

        for key, value in vd.items():
            if key == 'is_done':
                notes = notes.filter(is_done=value)
            elif key == 'time':
                notes = notes.filter(time__gte=value)
            elif key == 'priority':
                notes = notes.filter(priority__gte=value)
        # url?param1=value,value2
        # url?param1=value&param1=value2
        return Response(self.get_serializer(notes, many=True).data)

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
