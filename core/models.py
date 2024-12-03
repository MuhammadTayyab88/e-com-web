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
