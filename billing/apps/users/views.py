from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from apps.abonents.models import Abonent, UserEvent
from apps.users.forms import ChangeStatusContactForm, ChangeTarifContactForm


@login_required
def report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        # Преобразуйте строки в объекты datetime и сделайте их осведомленными
        start_date = timezone.make_aware(parse_datetime(start_date + "T00:00:00"))
        end_date = timezone.make_aware(parse_datetime(end_date + "T23:59:59"))
        
        user_events = UserEvent.objects.filter(
            Q(date__gte=start_date) & Q(date__lte=end_date)
        )
    else:
        user_events = UserEvent.objects.none()  # Или какой-то другой дефолтный QuerySet
    
    # Убедитесь, что QuerySet упорядочен перед пагинацией
    user_events = user_events.order_by('-date')

    paginator = Paginator(user_events, 10)  # Показывать 10 событий на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/report.html', {'page_obj': page_obj})


@login_required
def send_tarif(request):
    abonent = Abonent.objects.get(login=request.user)
    if request.method == 'POST':
        form = ChangeTarifContactForm(request.POST, account_number=abonent.account_number)
        if form.is_valid():
            name = abonent.name
            account_number = abonent.account_number
            tarif = form.cleaned_data['tarif']

            full_message = f"""
            Имя: {name}
            Номер договора: {account_number}
            Тариф: {tarif}
            """
            email_theme = f'Смена тарифа договор {account_number}'
            # Отправка сообщения
            send_mail(
                email_theme,  # Тема
                full_message,  # Сообщение
                settings.EMAIL_HOST_USER,  # От кого
                ['knets@yandex.ru'],  # Кому (список email адресов)
                fail_silently=False,
            )
            messages.success(request, 'Заявка на изменение тарифа отправлена!')
            return redirect('tarif')
        else:
            form = ChangeTarifContactForm(request.POST, account_number=abonent.account_number)
        # Форма не была отправлена, отображаем пустую форму
    else:
        form = ChangeTarifContactForm(account_number=abonent.account_number)

    return render(request, 'users/tarif.html', {'form': form})


@login_required
def send_status(request):
    abonent = Abonent.objects.get(login=request.user)
    if request.method == 'POST':
        form_block = ChangeStatusContactForm(request.POST)
        if form_block.is_valid():
            name = abonent.name
            account_number = abonent.account_number
            block_status = form_block.cleaned_data['block_status']

            full_message = f"""
            Имя: {name}
            Номер договора: {account_number}
            Статус: {block_status}
            """
            email_theme = f'{block_status} {account_number}'
            # Отправка сообщения
            send_mail(
                email_theme,  # Тема
                full_message,  # Сообщение
                settings.EMAIL_HOST_USER,  # От кого
                ['knets@yandex.ru'],  # Кому (список email адресов)
                fail_silently=False,
            )
            messages.success(request, 'Ваша заявка принята и будет обработана в течение 20 минут!')
            return redirect('block')
        else:
            form_block = ChangeStatusContactForm(request.POST)
        # Форма не была отправлена, отображаем пустую форму
    else:
        form_block = ChangeStatusContactForm()

    return render(request, 'users/block.html', {'form_block': form_block})
