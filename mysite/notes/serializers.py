from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_done = serializers.BooleanField(read_only=True)
    class Meta:
        model = Note
        fields = "__all__"

class FilterSerializer(serializers.Serializer):
    is_done = serializers.BooleanField(required=False)
    time = serializers.TimeField(required=False)
    priority = serializers.IntegerField(required=False)
    # class Meta:
        # fields = ['text', 'time', 'priority']
        # fields = "__all__"
