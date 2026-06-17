from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name