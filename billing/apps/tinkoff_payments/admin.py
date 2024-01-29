from django.contrib import admin

from .models import PaymentTinkoff


class PaymentTinkoffAdmin(admin.ModelAdmin):
    list_display = ('account', 'payment_id', 'status', 'amount', 'phone', 'email', 'date', 'stamp')


admin.site.register(PaymentTinkoff, PaymentTinkoffAdmin)
