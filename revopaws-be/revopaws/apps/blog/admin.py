from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogComment
from unfold.admin import ModelAdmin

class BlogCategoryAdmin(ModelAdmin):
    list_display = ('category_id', 'category_name', 'description')
    search_fields = ('category_name',)

class BlogPostAdmin(ModelAdmin):
    list_display = ('post_id', 'title', 'author', 'author_type', 'category', 'created_at', 'updated_at')
    list_filter = ('author_type', 'category', 'created_at')
    search_fields = ('title', 'author__username', 'author__email')

class BlogCommentAdmin(ModelAdmin):
    list_display = ('comment_id', 'post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'user__username', 'content')

admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
