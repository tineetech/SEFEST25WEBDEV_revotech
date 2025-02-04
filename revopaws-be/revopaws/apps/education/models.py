from django.db import models

class EducationalContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
