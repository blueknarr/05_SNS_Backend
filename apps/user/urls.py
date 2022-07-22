from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import (
    UserCreateView,
    UserLoginView,
    UserView
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserView.as_view(), name='user'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]