from django.contrib import admin
from django.urls import path

from user.views import UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view()),
]