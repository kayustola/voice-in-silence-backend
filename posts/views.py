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
import os
import resend
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer

resend.api_key = os.environ.get("RESEND_API_KEY")


class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact = serializer.save()

        resend.Emails.send({
            "from": "Voice in Silence <onboarding@resend.dev>",
            "to": [contact.email],
            "subject": "Thanks for contacting Voice in Silence",
            "html": f"""
            <h2>Hi {contact.name},</h2>

            <p>Thank you for reaching out to <strong>Voice in Silence</strong>.</p>

            <p>I have received your message and I'll get back to you as soon as possible.</p>

            <p>God bless you.</p>

            <br>

            <strong>Kayustola</strong><br>
            Voice in Silence
            """
        })