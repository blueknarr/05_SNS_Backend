from django.contrib import admin
from django.urls import path

from post.views import (
    PostView,
    PostDetailView,
    PostRestoreView
)

urlpatterns = [
    path('', PostView.as_view(), name='post'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('restore/', PostRestoreView.as_view(), name='post_restore'),
    path('restore/<int:post_id>/', PostRestoreView.as_view(), name='post_restore')
]