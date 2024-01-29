import calendar
from datetime import datetime, timedelta

from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from .event_writer import write_event_trust
from .models import Abonent, UserEvent


class UserEventAdmin(admin.ModelAdmin):
    list_display = ['abonent', 'date', 'event', 'new_balance', 'comment']
    list_filter = (('date', DateRangeFilter),)

    def get_list_display_links(self, request, list_display):
        return None


admin.site.register(UserEvent, UserEventAdmin)


class AbonentAdmin(admin.ModelAdmin):
    def user_actions(self, obj):
        return format_html(
            '<select onchange="window.location.href=this.value;">'
            '   <option value="">Выберите действие...</option>'
            '   <option value="{}">Пополнить счет</option>'
            '   <option value="{}">Показать события</option>'
            '</select>',
            # Пути к URL для каждого действия:
            reverse('add_funds_to_abonent', args=[obj.pk]),
            reverse('admin:abonents_userevent_changelist') + f'?abonent__id__exact={obj.pk}',
        )
    
    def add_funds_link(self, obj):
        return format_html('<a href="{}">Добавить средства</a>', reverse('add_funds_to_abonent', args=[obj.pk]))
    add_funds_link.short_description = 'Добавить средства'
    list_display = ('colored_name', 'account_number', 'login', 'password', 'colored_balance', 'group', 'user_actions')
    search_fields = ('account_number', 'name', 'login_mikrotik')
    actions = ['show_balance_statistics', 'download_log_file_mikrotik', 'download_log_file_lifestream', 'trust_payment']
    # list_per_page = 30

    def show_balance_statistics(self, request, queryset):
        positive_balance_count = Abonent.objects.filter(balance__gte=0).count()
        negative_balance_count = Abonent.objects.filter(balance__lt=0).count()
        total_count = Abonent.objects.all().count()

        self.message_user(request, f"Активные абоненты: {positive_balance_count}")
        self.message_user(request, f"Заблокированные абоненты: {negative_balance_count}")
        self.message_user(request, f"Общее количество абонентов: {total_count}")

        return HttpResponseRedirect(request.get_full_path())

    show_balance_statistics.short_description = "Показать статистику балансов"

    def download_log_file_mikrotik(self, request, queryset):
        log_file_path = 'utils/billing_scripts/logs/mikrotik_connection_errors.log'

        with open(log_file_path, 'rb') as log_file:
            response = HttpResponse(log_file.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename="mikrotik_logfile.log"'
            return response

    download_log_file_mikrotik.short_description = "Скачать отчет логов микротика"

    def download_log_file_lifestream(self, request, queryset):
        log_file_path = 'utils/lifestream/lifestream.log'

        with open(log_file_path, 'rb') as log_file:
            response = HttpResponse(log_file.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename="lifestream_logfile.log"'
            return response

    download_log_file_lifestream.short_description = "Скачать отчет логов смотрешки"

    def save(self, *args, **kwargs):
        # Если это новый объект и login_mikrotik не задан, установите его равным login
        if not self.pk and not self.login_mikrotik:
            self.login_mikrotik = self.login.username

        super().save(*args, **kwargs)

    def trust_payment(self, request, queryset):
        with transaction.atomic():
            current_month = datetime.now().strftime("%m")
            for abonent in queryset:
                if not abonent.credit_check or abonent.credit_check != current_month:
                    if abonent.balance < 0:
                        today = datetime.now()
                        end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
                        days_left_in_month = end_of_month.day - today.day
                        future_date = datetime.now() + timedelta(days=5)
                        formatted_date = future_date.strftime("%d-%m-%Y")
                        if days_left_in_month < 5:
                            trust_payment = - abonent.balance
                            abonent.balance += abonent.group.month_price - abonent.balance
                            write_event_trust(abonent, trust_payment, abonent.balance)
                            self.message_user(request, f"Доверительный платеж для абонента {abonent.name} на сумму {trust_payment} руб. взят.")
                            abonent.credit = f"{formatted_date}x{trust_payment}"
                            abonent.credit_check = f"{current_month}"
                        else:
                            trust_payment = - abonent.balance
                            abonent.balance += - abonent.balance
                            abonent.credit = f"{formatted_date}x{trust_payment}"
                            self.message_user(request, f"Доверительный платеж для абонента {abonent.name} на сумму {trust_payment} руб. взят.")
                            abonent.credit_check = f"{current_month}"
                            write_event_trust(abonent, trust_payment, abonent.balance)
                    else:
                        if abonent.balance < abonent.group.month_price:
                            future_date = datetime.now() + timedelta(days=5)
                            formatted_date = future_date.strftime("%d-%m-%Y")
                            new_balance = abonent.group.month_price
                            trust_payment = new_balance - abonent.balance
                            abonent.credit = f"{formatted_date}x{trust_payment}"
                            abonent.credit_check = f"{current_month}"
                            abonent.balance = new_balance
                            self.message_user(request, f"Доверительный платеж для абонента {abonent.name} на сумму {trust_payment} руб. взят.")
                            write_event_trust(abonent, trust_payment, abonent.balance)
                        else:
                            self.message_user(request, "Денег достаточно доверительный не нужен")
                else:
                    messages.error(request, "Доверительный платеж можно брать один раз в календарный месяц")
                abonent.save()

    trust_payment.short_description = "Взять доверительный"


admin.site.register(Abonent, AbonentAdmin)
