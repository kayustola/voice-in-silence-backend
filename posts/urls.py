from django.urls import path
from .views import (
    PostListView,
    CommentListCreateView,
    CommentUpdateView,
    CommentDeleteView,
    ContactCreateView
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),

    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('contact/', ContactCreateView.as_view(), name='contact'),
]