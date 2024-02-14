from django.contrib import admin

from .models import PaymentSberbank
from rangefilter.filters import DateRangeFilter


class PaymentSberbankAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_number', 'txn_id', 'status', 'amount', 'txn_date')
    search_fields = ('account_number', 'txn_id')
    list_filter = (('txn_date', DateRangeFilter),)

    def get_list_display_links(self, request, list_display):
        return None


admin.site.register(PaymentSberbank, PaymentSberbankAdmin)
