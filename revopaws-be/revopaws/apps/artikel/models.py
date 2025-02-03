from django.db import models

class ArtikelCategory(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('publish', 'Publish')
    ]

    name = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    created_by = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Artikel(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('publish', 'Publish')
    ]

    banner = models.ImageField()
    name = models.CharField(max_length=250)
    short_description = models.CharField(max_length=250)
    slug = models.SlugField()
    category = models.ForeignKey(ArtikelCategory, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='publish')
    created_by = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
