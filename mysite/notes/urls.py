from django.urls import path, include

from . import api
from .api import *
from rest_framework import routers
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.SimpleRouter()
router.register(r'note', NoteViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),

    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
    # path('v1/notelist/', NoteViewSet.as_view({'get': 'list'})),
    # path('v1/notelist/<int:pk>/', NoteViewSet.as_view({'get': 'update'}))
]
