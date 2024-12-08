from django.contrib.auth.models import User
from django.db import models

from ecommerce.models import BaseModel


class MainCategory(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    slogan = models.CharField(max_length=100, blank=True, null=True)
    cover_image = models.ImageField("categories/cover/", blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class SubCategory(BaseModel):
    main_category = models.ForeignKey(
        MainCategory, related_name="sub_category", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.main_category} --- {self.name}"


class Product(BaseModel):
    sub_category = models.ForeignKey(
        SubCategory, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True
    )
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True
    )
    rating = models.PositiveIntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.name}"


class ProductMedia(BaseModel):
    product = models.ForeignKey(
        Product, related_name="product_images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self) -> str:
        return f"{self.product}"



class Address(BaseModel):
    ADDRESS_TYPE_CHOICES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='shipping')
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.full_name} - {self.address_type.capitalize()} Address"


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.user}"

from django.utils import timezone

class Order(BaseModel):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online Payment'),
        ('cod', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Transfer'),
        ('wallet', 'Wallet Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='shipping_orders')
    billing_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='billing_orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status.capitalize()}"

    def mark_as_paid(self, transaction_id=None):
        """Mark the order as paid."""
        self.payment_status = 'paid'
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()

    def mark_as_shipped(self):
        """Mark the order as shipped."""
        self.status = 'shipped'
        self.save()

    def mark_as_delivered(self):
        """Mark the order as delivered."""
        self.status = 'delivered'
        self.save()
