# class HomePageImage(models.Model):
#     title = models.CharField(max_length=100, blank=True, null=True)
#     image = models.ImageField(upload_to="homepage_images/", blank=True, null=True)

#     def __str__(self):
#         return self.title if self.title else "Image"


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to="products/", null=True, blank=True)

#     rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

#     CATEGORY_CHOICES = [
#         ("Electronics", "Electronics"),
#         ("Fashion", "Fashion"),
#         ("Bags", "Bags"),
#         ("Jewellery", "Jewellery"),
#     ]

#     category = models.CharField(
#         max_length=50, choices=CATEGORY_CHOICES, default="Jewellery"
#     )

#     def __str__(self):
#         return self.name


# class TrackingOrder(models.Model):
#     STATUS_CHOICES = [
#         ("processing", "Processing"),
#         ("shipped", "Shipped"),
#         ("delivered", "Delivered"),
#         ("cancelled", "Cancelled"),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(
#         Product, through="TrackingOrderItem", related_name="tracking_orders"
#     )
#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default="processing"
#     )
#     tracking_number = models.CharField(max_length=50, blank=True, null=True)
#     tracking_url = models.URLField(blank=True, null=True)
#     order_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Tracking Order #{self.id} by {self.user.username}"


# class TrackingOrderItem(models.Model):
#     order = models.ForeignKey(TrackingOrder, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.product.name} x {self.quantity}"


# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.name}  x {self.quantity}"


# class Checkout(models.Model):
#     PAYMENT_CHOICES = [
#         ("cod", "Cash on Delivery"),
#         ("online", "Online Payment"),
#     ]

#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("processed", "Processed"),
#         ("shipped", "Shipped"),
#         ("delivered", "Delivered"),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     name = models.CharField(max_length=100)
#     address = models.TextField()
#     contact_number = models.CharField(max_length=20)
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
#     added_at = models.DateTimeField(auto_now_add=True)
#     verify_order = models.BooleanField(default=False)
#     dispatched = models.BooleanField(default=False)
#     order_date = models.DateTimeField(default=now)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

#     def __str__(self):
#         return (
#             f"Order for {self.user.username} - {self.product.name}  x {self.quantity} "
#             f"on {self.order_date}"
#         )

#     def confirm_order(self):
#         self.verify_order = True
#         self.save()

#     def dispatch_order(self):
#         if self.verify_order:
#             self.dispatched = True
#             self.save()
#         else:
#             raise ValueError("Order must be verified before dispatching.")


# class PhoneOTP(models.Model):
#     phone_number = models.CharField(max_length=15, unique=True)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.phone_number} - {self.otp}"
