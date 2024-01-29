from django.db import models

from apps.abonents.models import Abonent


class PaymentSberbank(models.Model):
    account = models.ForeignKey(Abonent, on_delete=models.CASCADE, related_name='sberbank_payments')
    txn_id = models.CharField(max_length=30, null=True, blank=True)
    txn_date = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Платеж Сбербанк'
        verbose_name_plural = 'Платежи Сбербанк'

    def __str__(self):
        return str(self.account)
