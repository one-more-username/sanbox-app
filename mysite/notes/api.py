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

    # TODO action with params for filtration.
    # __str__ __repr__ __len__ __add__ mustread #   https://nuancesprog.ru/p/10529/

    @extend_schema(
        # override default docstring extraction
        description='More descriptive text',
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(name='Is done', description='Filter by completeness', required=False, type=bool),
            OpenApiParameter(
                name='Priority',
                description='Filter by priority',
                required=False,
                type=int,
                # location=OpenApiParameter.QUERY,
                # examples=[
                #     OpenApiExample(
                #         'Example 1',
                #         summary='short optional summary',
                #         description='longer description',
                #         value='1993-08-23'
                #     ),
                # ],
            ),
            OpenApiParameter(name='Time', description='Filter by time', required=False, type=OpenApiTypes.TIME),
        ],
        # # provide Authentication class that deviates from the views default
        # auth=None,
        # # change the auto-generated operation name
        # operation_id=None,
        # # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        # operation=None,
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value={}
            ),
            OpenApiExample(
                'Example 2',
                # description='22longer description',
                value={
                    'is_done': 'value',
                    'time': 'value',
                    'priority': 'value'
                }
            ),
        ],
    )
    @action(methods=['post'], detail=False, url_path='filtered')
    def filtered(self, request, *args, **kwargs):
        owner = request.user.id

        serializer_class = FilterSerializer(data=request.data)

        if not serializer_class.is_valid(raise_exception=True):
            print(serializer_class.errors)
        else:
            print('validated data', serializer_class.validated_data)

        notes = Note.objects.filter(owner_id=owner)

        vd: dict = serializer_class.validated_data  # OrderedDict

        for key, value in vd.items():
            if key == 'is_done':
                notes = notes.filter(is_done=value)
            elif key == 'time':
                notes = notes.filter(time__gte=value)
            elif key == 'priority':
                notes = notes.filter(priority__gte=value)

        return Response(self.get_serializer(notes, many=True).data)

    # @extend_schema(
    #     parameters=[
    #         QuerySerializer,  # serializer fields are converted to parameters
    #         OpenApiParameter("nested", QuerySerializer),  # serializer object is converted to a parameter
    #         OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
    #         OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),  # path variable was overridden
    #     ],
    #     request=YourRequestSerializer,
    #     responses=YourResponseSerializer,
    #     # more customizations
    # )

    def get_queryset(self):
        """
        Optionally restricts the returned notes to a given user,
        by filtering against a `priority` query parameter in the URL.
        """
        params = self.request.query_params
        queryset = Note.objects.all()

        is_done = params.get('is_done')
        time = params.get('time')
        priority = params.get('priority')

        #   http://127.0.0.1:8000/api/v1/note/?is_done=_&priority=_&time=_

        if is_done is not (False or None):
            queryset = queryset.filter(is_done=is_done)
        elif priority is not None:
            queryset = queryset.filter(priority__gte=priority)
        elif time is not None:
            queryset = queryset.filter(time__gte=time)
        return queryset

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
