from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# POSTS
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(status="published").order_by("-created_at")


# COMMENTS (LIST + CREATE)
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        return Comment.objects.filter(post_id=post_id).order_by("-created_at") if post_id else Comment.objects.all()


# COMMENT UPDATE (EDIT)
class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# COMMENT DELETE
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings


class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

   def perform_create(self, serializer):
    serializer.save()

       