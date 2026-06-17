from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'featured_image',
            'category',
            'status',
            'created_at',
            'updated_at'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

        from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'