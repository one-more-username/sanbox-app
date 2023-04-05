from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiParameter
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Note
from .permissions import DoesntDone, IsOwnerOrReadOnly
from .serializers import NoteSerializer, FilterSerializer


# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    # permission_classes = (IsAuthenticatedOrReadOnly, DoesntDone,)

    # files for .gitignore?????
    # __str__ __repr__ __len__ __add__ mustread #   https://nuancesprog.ru/p/10529/

    @extend_schema(
        description='More descriptive text',
        summary='Filtration according parameters from url',
        tags=['filtration'],
        request=None,
        responses={200: NoteSerializer},
        external_docs={'url': 'detail', 'description': 'Some description about url'},
        # external_docs='detail',
        parameters=[
            OpenApiParameter(
                name="is_done",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                required=False
            ),
            OpenApiParameter(
                name="time",
                type=OpenApiTypes.TIME,
                location=OpenApiParameter.QUERY,
                required=False),
            OpenApiParameter(
                name="priority",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False),
        ],
    )
    @action(methods=['post'], detail=False, url_path='filter-by-url')
    def filter_by_url(self, request, *args, **kwargs):
        owner = request.user.id
        notes = Note.objects.filter(owner_id=owner)

        serializer_class = FilterSerializer(data=request.data)

        if not serializer_class.is_valid(raise_exception=True):
            print('ERROR', serializer_class.errors)
        else:
            print('VALIDATED DATA', serializer_class.validated_data)

        params = request.query_params

        s_params = FilterSerializer(data=params)

        if s_params.is_valid(raise_exception=True):
            is_done = s_params['is_done'].value
            time = s_params['time'].value
            priority = s_params['priority'].value

            if time is not None:
                notes = notes.filter(time__gte=time)
            elif priority is not None:
                notes = notes.filter(priority__gte=priority)
            elif is_done is not None:
                notes = notes.filter(is_done=is_done)

        return Response(self.get_serializer(notes, many=True).data)

    @extend_schema(
        description='More descriptive text',
        summary='Filtration according parameters from request.body',
        tags=['filtration'],
        request=FilterSerializer,
        responses={200: NoteSerializer},
        external_docs={'url': 'detail', 'description': 'Some description about url'},
    )
    @action(methods=['post'], detail=False, url_path='filter-by-body')
    def filter_by_body(self, request, *args, **kwargs):
        owner = request.user.id
        notes = Note.objects.filter(owner_id=owner)

        serializer_class = FilterSerializer(data=request.data)

        if not serializer_class.is_valid(raise_exception=True):
            print('ERROR', serializer_class.errors)
        else:
            print('VALIDATED DATA', serializer_class.validated_data)

        vd: dict = serializer_class.validated_data  # OrderedDict

        for key, value in vd.items():
            if key == 'is_done':
                notes = notes.filter(is_done=value)
            elif key == 'time':
                notes = notes.filter(time__gte=value)
            elif key == 'priority':
                notes = notes.filter(priority__gte=value)

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
