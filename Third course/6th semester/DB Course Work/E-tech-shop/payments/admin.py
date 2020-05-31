from django.contrib import admin
from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

    class Meta:
        model = Payment


admin.site.register(Payment, PaymentAdmin)


