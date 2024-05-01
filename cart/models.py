from django.contrib.auth.models import User
from django.db import models

from Product.models import Product
from account.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    is_paid = models.BooleanField(null=True,blank=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total=models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.email

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()

