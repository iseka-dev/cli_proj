from django.contrib import admin

# Register your models here.

from .models import Product, Order, OrderDetail

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
