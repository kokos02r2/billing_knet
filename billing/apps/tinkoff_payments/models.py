from django.db import models

from apps.abonents.models import Abonent


class PaymentTinkoff(models.Model):
    account = models.ForeignKey(Abonent, on_delete=models.CASCADE, related_name='tinkoff_payments')
    payment_id = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    stamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Платеж Тинькофф'
        verbose_name_plural = 'Платежи Тинькофф'

    def __str__(self):
        return str(self.account)
