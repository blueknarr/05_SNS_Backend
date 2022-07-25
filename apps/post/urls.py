from django.contrib import admin
from django.urls import path

from post.views import (
    PostView
)

urlpatterns = [
    path('', PostView.as_view(), name='post'),
    path('<int:post_id>', PostView.as_view(), name='post')
]