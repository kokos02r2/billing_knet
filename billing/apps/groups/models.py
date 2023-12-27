from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    bandwidth = models.CharField(max_length=100)
    month_price = models.DecimalField(max_digits=8, decimal_places=3)
    group_guid = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.group_name
