from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        # fields = ('text', 'is_done', 'time', 'priority', 'id')

    # text = serializers.CharField(max_length=255)
    # is_done = serializers.BooleanField(help_text='temp text')
    # time = serializers.TimeField()
    # priority = serializers.IntegerField()
    #
    # def create(self, validated_data):
    #     return Note.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.is_done = validated_data.get('is_done', instance.is_done)
    #     instance.time = validated_data.get('time', instance.time)
    #     instance.priority = validated_data.get('priority', instance.priority)
    #     instance.save()
    #
    #     return instance
