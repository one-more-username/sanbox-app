"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers

from profiles.views import UpdateProfileView, DetailProfileView
# from profiles.views import UserRegistrationView
from users.views import UserListView, UserCreateView, UserChangePasswordView

# from users.views import RegisterUserView

# from profiles.views import profile_page

router = routers.SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("notes.urls")),         #   http://127.0.0.1:8000/api/v1/notes/
    #
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    #
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('user/list/', UserListView.as_view(), name='list_all_users'),
    path('user/create/', UserCreateView.as_view(), name='create_new_user'),
    path('user/change_pass/', UserChangePasswordView.as_view(), name='change_user_password'),
    #
    path('profile/update/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/detail/<int:pk>/', DetailProfileView.as_view(), name='detail_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
