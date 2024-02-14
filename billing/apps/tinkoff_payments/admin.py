from django.contrib import admin

from .models import PaymentTinkoff
from rangefilter.filters import DateRangeFilter


class PaymentTinkoffAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_number', 'payment_id', 'status', 'amount', 'phone', 'email', 'date', 'stamp')
    search_fields = ('account_number', 'payment_id', 'phone')
    list_filter = (('date', DateRangeFilter),)

    def get_list_display_links(self, request, list_display):
        return None


admin.site.register(PaymentTinkoff, PaymentTinkoffAdmin)
