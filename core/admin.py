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

