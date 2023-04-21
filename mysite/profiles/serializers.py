from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(allow_blank=True, read_only=True)
    gender = serializers.CharField(max_length=1, allow_blank=True)
    image = serializers.ImageField(allow_empty_file=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = "__all__"
        # exclude = ('user', )

