from django.db import models


class TvIdentifier(models.Model):
    identifier = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'ТВ идентификатор'
        verbose_name_plural = 'ТВ идентификаторы'

    def __str__(self):
        return self.identifier


class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    bandwidth = models.CharField(max_length=100)
    month_price = models.DecimalField(max_digits=8, decimal_places=3)
    group_guid = models.CharField(max_length=200, null=True, blank=True)
    tv_identifiers = models.ManyToManyField(TvIdentifier, blank=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.group_name
