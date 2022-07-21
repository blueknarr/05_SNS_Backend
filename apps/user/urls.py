from django.contrib import admin
from django.urls import path

from user.views import (
    UserCreateView,
    UserLoginView
)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]