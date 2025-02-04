# Generated by Django 5.1.5 on 2025-02-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EducationalContent',
            fields=[
                ('content_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image_url', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
