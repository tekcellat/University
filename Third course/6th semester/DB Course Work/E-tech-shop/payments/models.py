from django.db import models
from orders.models import *


class Payment(models.Model):
    payment_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    order_name = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_nds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comments = models.TextField(blank=True, null=True, default=None)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.payment_name

    class Meta:
        verbose_name = 'Платежка'
        verbose_name_plural = 'Платежки'