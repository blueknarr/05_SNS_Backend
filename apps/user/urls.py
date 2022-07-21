from django.contrib import admin
from django.urls import path

from user.views import (
    UserCreateView,
    UserLoginView,
    UserView
)

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]