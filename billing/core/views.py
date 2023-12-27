from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from apps.abonents.models import Abonent, UserEvent
from decimal import Decimal
from django import forms
from django.http import HttpResponseRedirect
from django.db import transaction


@login_required
def profile(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    return render(request, 'users/profile.html', {'abonent': abonent})


@login_required
def profile_tarif(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    return render(request, 'users/profile_tarif.html', {'abonent': abonent})


@login_required
def trust_payment(request):
    if request.method == 'POST':
        abonent = get_object_or_404(Abonent, id=request.POST.get('abonent_id'))

        # Проверяем условия для доверительного платежа
        if abonent.credit_check is None and abonent.balance < Decimal('0'):
            # Вычисляем необходимую сумму, чтобы баланс стал 0
            amount_needed = -abonent.balance  # Сумма будет положительной
            abonent.balance += amount_needed
            abonent.save()  # Сохраняем изменения
            # Добавьте логику для регистрации доверительного платежа, если это необходимо

    return redirect('profile')   # Возвращаем п


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(label='Сумма', max_digits=10, decimal_places=3)


def add_funds_to_abonent(request, abonent_id):
    with transaction.atomic():
        abonent = Abonent.objects.get(id=abonent_id)
        if request.method == 'POST':
            form = AddFundsForm(request.POST)
            if form.is_valid():
                abonent.balance += form.cleaned_data['amount']
                abonent.save()
                event = [UserEvent(
                    abonent=abonent,
                    event=f"{form.cleaned_data['amount']} руб.",
                    comment=f"Добавлена сумма {form.cleaned_data['amount']} руб.",
                    new_balance=f"{abonent.balance} руб."
                )]
                UserEvent.objects.bulk_create(event)
                # Вернуться на страницу абонента после добавления средств
                return HttpResponseRedirect("/admin/abonents/abonent/")
        else:
            form = AddFundsForm()

        return render(request, 'admin/add_funds.html', {'form': form, 'abonent': abonent})
