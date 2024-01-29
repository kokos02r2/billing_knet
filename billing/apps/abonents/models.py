from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html

from apps.groups.models import Group

User = get_user_model()


class Abonent(models.Model):
    login = models.OneToOneField(User, on_delete=models.CASCADE)
    login_mikrotik = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200, unique=True)
    account_number = models.CharField(max_length=30, null=True, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    ip_addr = models.GenericIPAddressField(unique=True, null=True)
    block = models.BooleanField(default=False)
    create_date = models.DateField(null=True, blank=True)
    credit = models.CharField(max_length=200, null=True, blank=True)
    credit_check = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    passport = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def colored_balance(self):
        if self.balance < 0:
            return format_html(
                '<b><span style="color: #ff0000;">{}</span></b>',
                self.balance,
            )
        else:
            return format_html(
                '<b><span style="color: #008000;">{}</span></b>',
                self.balance,
            )

    colored_balance.short_description = 'Balance'

    def colored_name(self):
        if self.block:
            return format_html(
                '<b><span style="color: #ff0000;">{}</span></b>',
                self.name,
            )
        if self.balance < 0:
            return format_html(
                '<b><span style="color: #d4d4d4;">{}</span></b>',
                self.name,
            )
        else:
            return format_html(
                '<b><span style="color: #008000;">{}</span></b>',
                self.name,
            )

    colored_name.short_description = 'Name'

    class Meta:
        verbose_name = 'Абонент'
        verbose_name_plural = 'Абоненты'

    def __str__(self):
        return self.login.username


class UserEvent(models.Model):
    abonent = models.ForeignKey(Abonent, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)
    new_balance = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f"Event for {self.abonent.login} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
