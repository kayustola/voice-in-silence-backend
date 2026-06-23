from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings

from .models import Post, Comment, ContactMessage
from .serializers import (
    PostSerializer,
    CommentSerializer,
    ContactMessageSerializer
)

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


# COMMENT UPDATE
class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# COMMENT DELETE
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# CONTACT (FIXED)
class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact = serializer.save()

        # AUTO REPLY EMAIL
        try:
            send_mail(
                subject="Thanks for contacting Voice in Silence",
                message=f"""
Hi {contact.name},

Thanks for reaching out.

We received your message:
"{contact.message}"

We will get back to you soon.

— Voice in Silence
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=True,
            )
        except Exception:
            pass