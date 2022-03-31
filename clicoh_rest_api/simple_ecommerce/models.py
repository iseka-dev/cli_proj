from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=50,null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    date_time = models.DateTimeField(null=True, blank=True)

    def get_total(self):
        detail = OrderDetail.objects.get(order=self)
        return detail.product.price * detail.quantity

    def get_total_usd():
        pass

class OrderDetail(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=CASCADE
    )
    quantity = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
