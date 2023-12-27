from django.db import models
from django.contrib.auth import get_user_model
from apps.groups.models import Group


User = get_user_model()


class Abonent(models.Model):
    login = models.OneToOneField(User, on_delete=models.CASCADE)  # Ссылка на стандартную модель пользователя
    login_mikrotik = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200, unique=True)  # Название или имя
    account_number = models.CharField(max_length=30, null=True, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=3)  # Баланс
    group = models.ForeignKey(Group, on_delete=models.PROTECT)  # Связь с группой
    ip_addr = models.GenericIPAddressField(unique=True, null=True)  # IP-адрес
    block = models.BooleanField(default=False)  # Блокировка
    create_date = models.DateField(null=True, blank=True)  # Дата начала
    credit = models.CharField(max_length=200, null=True, blank=True)  # Кредит
    credit_check = models.CharField(max_length=30, null=True, blank=True)  # Проверка кредита
    email = models.EmailField(null=True, blank=True)  # Электронная почта
    phone = models.CharField(max_length=20, null=True, blank=True)  # Телефон
    address = models.TextField(null=True, blank=True)  # Адрес
    passport = models.CharField(max_length=50, null=True, blank=True)  # Паспортные данные
    description = models.TextField(blank=True, null=True)  # Описание

    class Meta:
        verbose_name = 'Абонент'  # Одиночное число
        verbose_name_plural = 'Абоненты'  # Множественное число

    def __str__(self):
        return self.login.username


class UserEvent(models.Model):
    abonent = models.ForeignKey(Abonent, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)
    new_balance = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = 'Событие'  # Одиночное число
        verbose_name_plural = 'События'  # Множественное число

    def __str__(self):
        return f"Event for {self.abonent.login} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
