from django import forms
from apps.groups.models import Group


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(label='Сумма', max_digits=10, decimal_places=3)


class BlockForm(forms.Form):
    CHOICES = [
        ('block', 'Блокировка'),
        ('unblock', 'Разблокировка')
    ]
    block = forms.ChoiceField(choices=CHOICES, label='Выберите действие')


class ChangeTarifForm(forms.Form):
    new_tariff = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by('group_name'),
        label='Выберите тариф'
    )
