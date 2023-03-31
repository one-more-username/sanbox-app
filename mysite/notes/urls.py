from .api import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'note', NoteViewSet)

urlpatterns = [
    # path('note/<int:id>/done', NoteAPISetDone.as_view()),
    # path('note/', NoteAPIList.as_view()),
    # path('notes/<int:pk>/', NoteAPIUpdate.as_view()),
    # path('notedelete/<int:pk>/', NoteAPIDestroy.as_view()),
]
urlpatterns += router.urls
