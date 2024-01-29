from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from apps.abonents.models import Abonent, UserEvent

from .trust_payment import set_trust_payment


@login_required
def profile(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    current_month = str(datetime.now().month).zfill(2)
    if abonent.credit:
        credit_parts = abonent.credit.split('x')
        if len(credit_parts) == 2:
            credit_date = credit_parts[0]
            credit_amount = credit_parts[1]
            
            # Преобразуем дату в желаемый формат, если необходимо
            try:
                credit_date = datetime.strptime(credit_date, '%d-%m-%Y').strftime('%d.%m.%Y')
            except ValueError:
                # Обработка неправильного формата даты
                credit_date = credit_date
            
            abonent.credit_formatted = f"до {credit_date} на сумму {credit_amount} руб."
        else:
            # Если строка не соответствует ожидаемому формату
            abonent.credit_formatted = "Некорректные данные"
    else:
        abonent.credit_formatted = None
    return render(request, 'users/user_profile.html', {'abonent': abonent, 'current_month': current_month})


@login_required
def payment(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    return render(request, 'users/payment.html', {'abonent': abonent})


@login_required
def trust_payment(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    message = set_trust_payment(abonent=abonent)
    messages.success(request, message)
    return redirect('profile')


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(label='Сумма', max_digits=10, decimal_places=3)


def add_funds_to_abonent(request, abonent_id):
    with transaction.atomic():
        abonent = Abonent.objects.get(id=abonent_id)
        if request.method == 'POST':
            form = AddFundsForm(request.POST)
            if form.is_valid():
                abonent.balance = abonent.balance + form.cleaned_data['amount']
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
