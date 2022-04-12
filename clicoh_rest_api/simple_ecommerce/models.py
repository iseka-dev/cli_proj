import requests as req
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

# Create your models here.


class Product(models.Model):
    """
    A class to represent products.

    ...

    Attributes
    ----------
    id : str
        product id

    name : int
        product name

    price : float
        product price

    stock : int
        amount of available products
    """

    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=50,null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    @receiver(post_save, sender='simple_ecommerce.OrderDetail')
    def update_stock(instance, created, **kwargs):
        if created is True:
            product = instance.product
            quantity = instance.quantity
            product.stock -= quantity
            product.save()
            return print('stock has been updated')
        else:
            return None

    @receiver(post_delete, sender='simple_ecommerce.OrderDetail')
    def fix_stock(instance, **kwargs):
        product = instance.product
        quantity = instance.quantity
        product.stock += quantity
        product.save()
        return print('stock has been updated')


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Order Nº' + str(self.id)

    def get_total(self):
        detail = OrderDetail.objects.filter(order=self)
        return sum([d.product.price * d.quantity for d in detail])

    def get_total_usd(self):
        usd_ars_change = req.get(
            'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        ).json()[0]['casa']['venta']
        return round(self.get_total() / int(usd_ars_change.split(',')[0]),2)

class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='details'
    )
    quantity = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    """@receiver(pre_save, sender='simple_ecommerce.OrderDetail')
    def check_repeated_product(instance, **kwargs):
        product = instance.product
        quantity = instance.quantity
        product.stock += quantity
        product.save()
        return print('stock has been updated')"""
