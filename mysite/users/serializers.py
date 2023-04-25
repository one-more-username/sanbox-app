from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User

from profiles.serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    # user fields
    first_name = serializers.CharField(default='John')
    last_name = serializers.CharField(default='Johnson')
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # profile fields
    gender = serializers.CharField(max_length=1, default='M')
    birthdate = serializers.DateField(allow_null=True)
    profile = ProfileSerializer(write_only=True, required=False)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'password2',
            'gender',
            'birthdate',
            'profile'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User(username=validated_data['username'])

        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    model = User

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    # check pass, set pass

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    # update
    def create(self, validated_data):
        user = User(username=validated_data['username'])

        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')


    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #     self._password = raw_password
    #
    # def check_password(self, raw_password):
    #     """
    #     Return a boolean of whether the raw_password was correct. Handles
    #     hashing formats behind the scenes.
    #     """
    #
    #     def setter(raw_password):
    #         self.set_password(raw_password)
    #         # Password hash upgrades shouldn't be considered password changes.
    #         self._password = None
    #         self.save(update_fields=["password"])
    #
    #     return check_password(raw_password, self.password, setter)
