from django.db import models


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    supplier_country = models.CharField(max_length=64, blank=True, null=True, default=None)
    supplier_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    supplier_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    supplier_email = models.EmailField(blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.supplier_name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE,)
#     image = models.ImageField(upload_to='products_images/')
#     is_active = models.BooleanField(default=True)
#     created = models.DateField(auto_now_add=True, auto_now=False)
#     updated = models.DateField(auto_now_add=False, auto_now=True)
#
#     def __str__(self):
#         return "%s" % self.id
#
#     class Meta:
#         verbose_name = 'Фотографии'
#         verbose_name_plural = 'Фотографии'
