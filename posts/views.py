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
            "to": ["voiceinsilence07@gmail.com"],
            "subject": f"📩 New Contact Form Submission from {contact.name}",
            "html": f"""
            <h2>New Contact Form Submission</h2>

            <p><strong>Name:</strong> {contact.name}</p>

            <p><strong>Email:</strong> {contact.email}</p>

            <p><strong>Message:</strong></p>

            <p>{contact.message}</p>

            <hr>

            <p>Sent from your Voice in Silence website.</p>
            """
        })