from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

# class AccountsConfig(AppConfig):
#     name = 'accounts'
#
#     def ready(self):
#         import accounts.signals
