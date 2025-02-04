from django.contrib import admin
from .models import Product, ProductReview, Order, OrderItem, Invoice, Shipping
from unfold.admin import ModelAdmin

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price', 'stock_quantity', 'category', 'created_at']
    search_fields = ['name']
    list_filter = ['category']


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username']

    list_filter = ['rating']

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['user', 'total_price', 'payment_status', 'shipping_status', 'created_at']
    search_fields = ['user__username', 'doctor__user__username']

    list_filter = ['payment_status', 'shipping_status']

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ['order', 'user', 'amount_due', 'status', 'due_date']
    search_fields = ['order__id', 'user__username']

    list_filter = ['status']

@admin.register(Shipping)
class ShippingAdmin(ModelAdmin):
    list_display = ['order', 'courier_name', 'shipping_status', 'estimated_date']
    search_fields = ['order__id', 'courier_name']

    list_filter = ['shipping_status']
