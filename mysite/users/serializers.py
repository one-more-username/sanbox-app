from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

        # fields = '__all__'


class PasswordSerializer(serializers.Serializer):
    # check pass, set pass

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

    pass
    # class Meta:
    #     model = User
    #     fields = ['password', ]
