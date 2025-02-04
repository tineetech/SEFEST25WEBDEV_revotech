from django.db import models
from django.conf import settings

class ForumCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.category_name


class ForumTopic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_topics'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(
        ForumCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='forum_topics'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        ForumTopic,
        on_delete=models.CASCADE,
        related_name='forum_posts'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_posts'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on topic '{self.topic.title}'"
