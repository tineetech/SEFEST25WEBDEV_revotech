from django.contrib import admin
from .models import ForumCategory, ForumTopic, ForumPost
from unfold.admin import ModelAdmin

class ForumCategoryAdmin(ModelAdmin):
    list_display = ('category_id', 'category_name', 'description')
    search_fields = ('category_name',)

class ForumTopicAdmin(ModelAdmin):
    list_display = ('topic_id', 'title', 'user', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')

class ForumPostAdmin(ModelAdmin):
    list_display = ('post_id', 'topic', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('topic__title', 'user__username', 'content')

admin.site.register(ForumCategory, ForumCategoryAdmin)
admin.site.register(ForumTopic, ForumTopicAdmin)
admin.site.register(ForumPost, ForumPostAdmin)
