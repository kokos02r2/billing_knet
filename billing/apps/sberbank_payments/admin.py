from django.contrib import admin

from .models import PaymentSberbank


class PaymentSberbankAdmin(admin.ModelAdmin):
    list_display = ('account', 'txn_id', 'status', 'amount', 'txn_date')


admin.site.register(PaymentSberbank, PaymentSberbankAdmin)
