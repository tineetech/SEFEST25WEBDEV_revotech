from django.contrib import admin
from apps.artikel.models import Artikel, ArtikelCategory
from unfold.admin import ModelAdmin

@admin.register(Artikel)
class ArtikelAdmin(ModelAdmin):
    list_display = ('name', 'banner', 'category', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(ArtikelCategory)
class ArtikelCategoryAdmin(ModelAdmin):
    list_display = ('name', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)