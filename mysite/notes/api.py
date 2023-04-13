from django.db.models import QuerySet, Prefetch, Count, Case, When, IntegerField, Avg
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Note, SubNote
from .permissions import DoesntDone, IsOwnerOrReadOnly
from .serializers import NoteSerializer, FilterSerializer, SubNoteSerializer
from .utils import query_debugger


# Create your views here.
class SubNoteViewSet(viewsets.ModelViewSet):
    queryset = SubNote.objects.select_related("from_note")
    # queryset = SubNote.objects.all()
    serializer_class = SubNoteSerializer
    # permission_classes = (AllowAny, )


class NoteViewSet(viewsets.ModelViewSet):
    # queryset = Note.objects.all()
    queryset = Note.objects.annotate(
        subnotes_quantity=Count("subnotes"),
        undoned_subnotes=Count(
            Case(When(subnotes__is_done=False, then=1), output_field=IntegerField())
        ),
        avg_subnotes_time_estimate=Avg("subnotes__estimated_time"),
        avg_subnotes_time_spent=Avg("subnotes__spent_time"),
    ).prefetch_related(
        "subnotes",
        Prefetch("subnotes", queryset=SubNote.objects.filter(is_done=True), to_attr="doned"),
        # Prefetch("subnotes", queryset=Note.objects.annotate(subnotes_quantity=Count("subnotes")), to_attr="subnotes_quantity")
    )
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    # permission_classes = (IsAuthenticatedOrReadOnly, DoesntDone,)

    @query_debugger
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # , context={'user': request.user, 'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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

            is_done = s_params.validated_data['is_done']
            time = s_params.validated_data['time']
            priority = s_params.validated_data['priority']

            if is_done is not None:
                notes = notes.filter(is_done=is_done)
            elif time is not None:
                notes = notes.filter(time__gte=time)
            elif priority is not None:
                notes = notes.filter(priority__gte=priority)

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
