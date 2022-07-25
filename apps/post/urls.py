from django.contrib import admin
from django.urls import path

from post.views import (
    PostView,
    PostDetailView,
)

urlpatterns = [
    path('', PostView.as_view(), name='post'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
]