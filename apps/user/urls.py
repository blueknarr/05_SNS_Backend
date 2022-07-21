from django.contrib import admin
from django.urls import path

from user.views import (
    UserCreateView,
    UserView
)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserView.as_view(), name='register'),
]