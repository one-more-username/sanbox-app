from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from datetime import datetime

from .models import Note


#   fields of model, serializer and they methods
#   methods of queryset, related() prefetch()
#   related tables
#   types ManyToMany, OneToMany, .......
#   add table SubNotes { is_done: bool, text: str }

# def priority_restriction(priority: int):
#     # user = get_user_model()
#     notes = Note.objects.all()  # or owner?
#     if len(notes.filter(priority=priority)):
#         raise serializers.ValidationError("Priority of notes cannot be repeated!")
#     return priority


def text_restriction(text: str):
    numbers = 0
    for symbol in text:
        if symbol.isdigit():
            if numbers == 2:
                raise serializers.ValidationError("Text can`t contain more than 2 numbers!")
            numbers += 1
    # numbers = sum(symbol.isdigit() for symbol in text)
    return text


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # is_done = serializers.BooleanField(read_only=True, validators=)
    is_done = serializers.BooleanField(required=False)

    # 1. validation by priority. not allow equal priority
    # 2. max numbers in note.text can't be more than 2
    class Meta:
        model = Note
        fields = "__all__"
        extra_kwargs = {
            'done_at': {'required': False},
            'time': {'required': False},
            # 'priority': {'validators': [priority_restriction]},
            'text': {'validators': [text_restriction]}
        }

    def validate(self, values):
        is_done = values.get('is_done')
        time = values.get('time')
        current_time = timezone.now().time()

        if is_done and (time is not None) and (time > current_time):
            raise serializers.ValidationError("ERROR! How it can be done in future?")

        # if (time is not None) and (time > current_time):
        #     raise serializers.ValidationError("ERROR! Marty, what year is it now?")

        # new note only with is_done=false
        # and
        # newnote can't create with time greater than current
        return values

    def validate_priority(self, value):
        user = self.context['request'].user

        # note_exist = Note.objects.filter(owner=user, priority=value).exist()  # or owner?

        if Note.objects.filter(owner=user, priority=value).exists():
            raise serializers.ValidationError("Priority of notes cannot be repeated!")

        # if len(notes.filter(priority=value)) is not 0:
        #     raise serializers.ValidationError("Priority of notes cannot be repeated!")
        # context?
        return value

    def validate_done_at(self, value):
        current_time = timezone.now()

        if value > current_time:
            raise serializers.ValidationError("!!!!ERROR! Marty, what year is it now?")
        return value


class FilterSerializer(serializers.Serializer):
    is_done = serializers.BooleanField(required=False, default=None, allow_null=True)
    time = serializers.TimeField(required=False, default=None)
    priority = serializers.IntegerField(required=False, default=None)
