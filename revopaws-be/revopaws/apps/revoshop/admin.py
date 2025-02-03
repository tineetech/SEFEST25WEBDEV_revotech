from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.revoshop.models import ProductCategory, Product

@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)
    
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'status', 'created_by')
    list_filter = ('status', 'category')
    search_fields = ('name', 'category__name')