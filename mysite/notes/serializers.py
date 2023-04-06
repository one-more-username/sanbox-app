from django.utils import timezone
from rest_framework import serializers
from datetime import datetime

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        extra_kwargs = {
            'done_at': {'required': False},
            # 'is_done': {'required': False},
            # 'time': {'required': False},
            }

    def validate(self, values):
        if values['is_done']:
            raise serializers.ValidationError("ERROR! How it can be done?")

        current_time = timezone.now()   #   this can raise error
        if values['time'] > current_time:
            raise serializers.ValidationError("ERROR! Marty, what year is it now?")

        # new note only with is_done=false
        # new note can't create with time greater than current
        return values

    def validate_done_at(self, value):
        current_time = timezone.now()

        if value > current_time:
            raise serializers.ValidationError("ERROR! Marty, what year is it now?")
        return value


class FilterSerializer(serializers.Serializer):
    is_done = serializers.BooleanField(required=False, default=None, allow_null=True)
    time = serializers.TimeField(required=False, default=None)
    priority = serializers.IntegerField(required=False, default=None)
