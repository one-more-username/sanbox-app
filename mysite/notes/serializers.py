from django.utils import timezone
from rest_framework import serializers

from .models import Note, SubNote


def text_restriction(text: str):
    numbers = 0
    for symbol in text:
        if symbol.isdigit():
            if numbers == 2:
                raise serializers.ValidationError("Text can`t contain more than 2 numbers!")
            numbers += 1
    return text


class SubNoteSerializer(serializers.ModelSerializer):
    is_done = serializers.BooleanField(default=False)
    text = serializers.CharField()

    class Meta:
        model = SubNote
        exclude = ('from_note',)
        extra_kwargs = {
            'is_done': {'required': False},
            'estimated_time': {'required': False},
        }


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_done = serializers.BooleanField(required=False)
    subnotes = SubNoteSerializer(many=True, read_only=True)  # allow_null=True?
    doned = SubNoteSerializer(many=True, read_only=True)
    subnotes_quantity = serializers.IntegerField()
    undoned_subnotes = serializers.IntegerField()
    avg_subnotes_time_estimate = serializers.FloatField()
    avg_subnotes_time_spent = serializers.FloatField()

    # def get_subnotes_quantity(self, instance):
    #     pass
    #
    # def get_undoned_subnotes(self, instance):
    #     pass
    #
    # def get_avg_subnotes_time_estimate(self, instance):
    #     pass
    #
    # def get_avg_subnotes_time_spent(self, instance):
    #     pass

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
        return values

    def validate_priority(self, value):
        user = self.context['request'].user

        if Note.objects.filter(owner=user, priority=value).exists():
            raise serializers.ValidationError("Priority of notes cannot be repeated!")
        return value

    def validate_done_at(self, value):
        current_time = timezone.now()

        if value > current_time:
            raise serializers.ValidationError("!!!!ERROR! Marty, what year is it now?")
        return value


class SubNoteSerializer(serializers.ModelSerializer):
    is_done = serializers.BooleanField()

    # text = serializers.TextField()
    # from_note = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SubNote
        fields = "__all__"


class FilterSerializer(serializers.Serializer):
    is_done = serializers.BooleanField(required=False, default=None, allow_null=True)
    time = serializers.TimeField(required=False, default=None)
    priority = serializers.IntegerField(required=False, default=None)
