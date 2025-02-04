from django.db import models
from django.conf import settings

class BlogCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.category_name


class BlogPost(models.Model):
    POST_AUTHOR_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    ]

    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    author_type = models.CharField(max_length=10, choices=POST_AUTHOR_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content_preview = models.CharField(max_length=255)
    content = models.TextField()
    meta_tag = models.TextField(blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Validasi: Hanya admin atau dokter yang bisa membuat blog
        if self.author.role not in ['admin', 'doctor']:
            raise ValueError("Only admins and doctors can create blog posts.")
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
