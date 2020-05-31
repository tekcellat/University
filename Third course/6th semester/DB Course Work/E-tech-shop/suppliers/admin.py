from django.contrib import admin
from .models import *


class SupplierAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supplier._meta.fields]

    class Meta:
        model = Supplier


admin.site.register(Supplier, SupplierAdmin)


