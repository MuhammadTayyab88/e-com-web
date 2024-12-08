from django.contrib import admin
from django.utils import timezone

from .models import *

# Registering models

admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductMedia)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Order)


# admin.site.register(HomePageImage)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'description', 'price', 'image', 'rating')
#     search_fields = ('name', 'description', 'category')
#     list_filter = ('category', 'price', 'rating')

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     # Ensure size is not in this list
#     list_display = ('user', 'product', 'quantity', 'product_category', 'added_at')
#     search_fields = ('user__username', 'product__name')
#     list_filter = ('product__category', 'added_at')

#     def product_category(self, obj):
#         return obj.product.category
#     product_category.short_description = 'Product Category'

# @admin.register(Checkout)
# class CheckoutAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'name','product', 'payment_method', 'order_date','verify_order','dispatched']
#     list_filter = ['payment_method', 'order_date']
#     search_fields = ['user__username', 'name', 'contact_number', 'address']
#     actions = ['mark_as_processed']

#     def mark_as_processed(self, request, queryset):
#         for checkout in queryset:
#             # Mark the order as verified
#             checkout.verify_order = True
#             checkout.save()

#             # Create a TrackingOrder for the verified Checkout order
#             tracking_order = TrackingOrder.objects.create(
#                 user=checkout.user,
#                 status='processing',  # Default status
#                 tracking_number=f'TRCK{checkout.id}',  # Example tracking number format
#                 order_date=timezone.now()
#             )

#             # Create a TrackingOrderItem for each product in the Checkout order
#             TrackingOrderItem.objects.create(
#                 order=tracking_order,
#                 product=checkout.product,
#                 quantity=checkout.quantity
#             )

#         # Display a success message in the admin interface
#         self.message_user(request, "Verified Checkout ID for tracking.")

#     mark_as_processed.short_description = "Mark selected checkouts as processed and create tracking orders"


# # trackong order
# class TrackingOrderItemInline(admin.TabularInline):
#     model = TrackingOrderItem
#     extra = 0  # No extra empty rows in the inline form

# @admin.register(TrackingOrder)
# class TrackingOrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'status', 'tracking_number', 'order_date']
#     list_filter = ['status', 'order_date']
#     search_fields = ['user__username', 'tracking_number']
#     inlines = [TrackingOrderItemInline]  # Embed TrackingOrderItem as inline

#     actions = ['mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']

#     def mark_as_shipped(self, request, queryset):
#         queryset.update(status='shipped')
#         self.message_user(request, "Selected orders marked as shipped.")

#     def mark_as_delivered(self, request, queryset):
#         queryset.update(status='delivered')
#         self.message_user(request, "Selected orders marked as delivered.")

#     def mark_as_cancelled(self, request, queryset):
#         queryset.update(status='cancelled')
#         self.message_user(request, "Selected orders marked as cancelled.")

#     # Short descriptions for actions
#     mark_as_shipped.short_description = "Mark selected orders as Shipped"
#     mark_as_delivered.short_description = "Mark selected orders as Delivered"
#     mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

# # Optional registration of TrackingOrderItem directly if needed independently
# @admin.register(TrackingOrderItem)
# class TrackingOrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity']
#     list_filter = ['order__status']
#     search_fields = ['order__tracking_number', 'product__name']
