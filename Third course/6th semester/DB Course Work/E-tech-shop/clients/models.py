from django.db import models


class Client(models.Model):
    client_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    client_country = models.CharField(max_length=64, blank=True, null=True, default=None)
    client_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    client_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    client_email = models.EmailField(blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.client_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

