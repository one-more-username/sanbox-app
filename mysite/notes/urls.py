from django.urls import path, include

from . import api
from .api import *
from rest_framework import routers
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.SimpleRouter()
router.register(r'note', NoteViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
