from django.contrib import admin
from django.urls import path

from post.views import (
    PostCreateView,
    PostView
)

urlpatterns = [
    path('', PostView.as_view(), name='post'),
    path('create/', PostCreateView.as_view(), name='create_post'),
]