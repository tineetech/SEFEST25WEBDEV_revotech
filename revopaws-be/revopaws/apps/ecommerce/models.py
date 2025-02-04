from django.db import models
from django.conf import settings
from apps.consultation.models import Consultation
from apps.users.models import Doctor

# Model Produk
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('medicine', 'Medicine'),
        ('equipment', 'Equipment'),
        ('food', 'Food')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Model Ulasan Produk
class ProductReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='product_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


# Model Order
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders'
    )
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders'
    )
    consultation_type = models.CharField(max_length=10, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    verification_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        blank=True, null=True
    )
    shipping_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('on_the_way', 'On the Way'),
            ('delivered', 'Delivered'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        blank=True, null=True
    )
    estimated_delivery = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# Model Item Pesanan
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"


# Model Pengiriman
class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    courier_name = models.CharField(max_length=255)
    tracking_number = models.CharField(max_length=255)
    shipping_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('on_the_way', 'On the Way'),
            ('delivered', 'Delivered')
        ],
        default='pending'
    )
    estimated_date = models.DateField()

    def __str__(self):
        return f"Shipping for Order #{self.order.id} - {self.courier_name}"


# Model Invoice
class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ('issued', 'Issued'),
            ('paid', 'Paid'),
            ('overdue', 'Overdue')
        ],
        default='issued'
    )

    def __str__(self):
        return f"Invoice #{self.id} for Order #{self.order.id}"
