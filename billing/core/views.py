from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
import calendar

from apps.abonents.models import Abonent, UserEvent
from core.forms import AddFundsForm, BlockForm, ChangeTarifForm

from core.helpers.trust_payment_logic import set_trust_payment
from core.helpers.сhange_tarif import change_tarif_logic


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


@staff_member_required
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


def get_days_left_in_month():
    current_date = datetime.now()
    first_day_of_next_month = current_date.replace(day=1, month=current_date.month + 1)
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    if current_date.month == 12:
        first_day_of_next_month = first_day_of_next_month.replace(year=current_date.year + 1, month=1)
    days_left_in_month = (first_day_of_next_month - current_date).days
    return days_left_in_month, days_in_month


@staff_member_required
def block_abonent(request, abonent_id):
    with transaction.atomic():
        abonent = Abonent.objects.get(id=abonent_id)
        if request.method == 'POST':
            form = BlockForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['block'] == 'block':
                    abonent.block = True
                if form.cleaned_data['block'] == 'unblock':
                    abonent.block = False
                abonent.save()
                event = [UserEvent(
                    abonent=abonent,
                    event=f"{form.cleaned_data['block']}",
                    comment=f"{form.cleaned_data['block']}",
                    new_balance=f"{abonent.balance} руб."
                )]
                UserEvent.objects.bulk_create(event)
                # Вернуться на страницу абонента после добавления средств
                return HttpResponseRedirect("/admin/abonents/abonent/")
        else:
            form = BlockForm()

        return render(request, 'admin/block.html', {'form': form, 'abonent': abonent})


@staff_member_required
def change_tarif(request, abonent_id):
    with transaction.atomic():
        abonent = Abonent.objects.get(id=abonent_id)
        if request.method == 'POST':
            form = ChangeTarifForm(request.POST)
            try:
                if form.is_valid():
                    new_tariff = form.cleaned_data['new_tariff']
                    change_tarif_logic(abonent, new_tariff)
                    messages.success(request, 'Тариф успешно изменен!')
                    return HttpResponseRedirect("/admin/abonents/abonent/")
            except Exception as e:
                messages.error(request, f'Ошибка при изменении тарифа: {e}')
        else:
            form = ChangeTarifForm()

        return render(request, 'admin/change_tarif.html', {'form': form, 'abonent': abonent})
