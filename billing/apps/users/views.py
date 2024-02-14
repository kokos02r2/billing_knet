from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404


from apps.abonents.models import Abonent, UserEvent
from apps.users.forms import ChangeStatusContactForm, ChangeTarifContactForm
from apps.users.send_email import send_abonent_mail


@login_required
def report(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = timezone.make_aware(parse_datetime(start_date + "T00:00:00"))
        end_date = timezone.make_aware(parse_datetime(end_date + "T23:59:59"))
        user_events = UserEvent.objects.filter(
            Q(date__gte=start_date) & Q(date__lte=end_date) & Q(abonent=abonent)
        )
    else:
        user_events = UserEvent.objects.none()

    user_events = user_events.order_by('-date')
    paginator = Paginator(user_events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/report.html', {'page_obj': page_obj})


@login_required
def send_tarif(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    if request.method == 'POST':
        form = ChangeTarifContactForm(request.POST, account_number=abonent.account_number)
        if form.is_valid():
            send_abonent_mail(abonent, form.cleaned_data['tarif'], 'Смена тарифа')
            messages.success(request, 'Заявка на изменение тарифа отправлена!')
            return redirect('tarif')
    else:
        form = ChangeTarifContactForm(account_number=abonent.account_number)

    return render(request, 'users/tarif.html', {'form': form})


@login_required
def send_status(request):
    abonent = get_object_or_404(Abonent, login=request.user)
    if request.method == 'POST':
        form_block = ChangeStatusContactForm(request.POST)
        if form_block.is_valid():
            send_abonent_mail(abonent, form_block.cleaned_data['block_status'], 'Изменение статуса')
            messages.success(request, 'Ваша заявка принята и будет обработана в течение 20 минут!')
            return redirect('block')
    else:
        form_block = ChangeStatusContactForm()

    return render(request, 'users/block.html', {'form_block': form_block})
