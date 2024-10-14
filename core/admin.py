from django.contrib import admin
from .models import Product, CartItem, Checkout, TrackingOrderItem, HomePageImage


# Registering models
admin.site.register(HomePageImage)
admin.site.register(TrackingOrderItem)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'price', 'image', 'rating')
    search_fields = ('name', 'description', 'category')
    list_filter = ('category', 'price', 'rating')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'size', 'quantity', 'product_category', 'added_at')
    search_fields = ('user__username', 'product__name', 'size')
    list_filter = ('product__category', 'added_at')

    def product_category(self, obj):
        return obj.product.category
    product_category.short_description = 'Product Category'

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'payment_method', 'order_date']
    list_filter = ['payment_method', 'order_date']
    search_fields = ['user__username', 'name', 'contact_number', 'address']
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        queryset.update(status='processed')  # Assuming you have a status field
        self.message_user(request, "Selected checkouts have been marked as processed.")
    mark_as_processed.short_description = "Mark selected checkouts as processed"
