from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(allow_blank=True)
    birthdate = serializers.DateField()
    gender = serializers.CharField(max_length=1, allow_blank=True)
    image = serializers.ImageField(allow_empty_file=True, allow_null=True)

    class Meta:
        model = Profile
        fields = "__all__"
