from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.marketplace.models import Product, ProductCategory, Order

@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'seller', 'price_cash', 'price_coin', 'status', 'stock')
    list_filter = ('status', 'category')
    search_fields = ('name', 'seller__username', 'category__name')

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('product', 'buyer', 'totals_cash', 'totals_coin', 'status')
    list_filter = ('status',)
    search_fields = ('product__name', 'buyer__username')
