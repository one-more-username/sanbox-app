from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_done = serializers.BooleanField(read_only=True)
    class Meta:
        model = Note
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     note = Note.objects.get(pk=instance.id)
    #     Note.objects.filter(pk=instance.id).update(**validated_data)
    #     return note
    # def update(self, instance, validated_data):

        # return

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance