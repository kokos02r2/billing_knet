import os
import sys
from django.db.models import Sum, Case, When, CharField, Value
import django
from django.utils import timezone
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.tinkoff_payments.models import PaymentTinkoff
from apps.sberbank_payments.models import PaymentSberbank


def write_payment_report(model, start_date, end_date, report_file_path):
    date_field_name = 'txn_date' if model == PaymentSberbank else 'date'

    payments = model.objects.filter(
        **{f'{date_field_name}__range': [start_date, end_date]},
        status__in=['CONFIRMED', 'pay'] if model == PaymentSberbank else ['CONFIRMED']
    )

    payments = payments.annotate(
        settlement=Case(
            When(account_number__range=("880000", "880999"), then=Value('Октябрьский')),
            When(account_number__range=("888000", "888999"), then=Value('Октябрьский')),
            When(account_number__range=("881000", "881999"), then=Value('Саваслейка')),
            When(account_number__range=("882000", "882099"), then=Value('Юганец')),
            When(account_number__range=("883000", "883399"), then=Value('WIFI')),
            When(account_number__range=("883400", "883499"), then=Value('Дуденево_GPON')),
            When(account_number__range=("883700", "883799"), then=Value('Дуденево_GPON')),
            When(account_number__range=("883500", "883699"), then=Value('Октябрьский_GPON')),
            When(account_number__range=("883800", "883899"), then=Value('Октябрьский_GPON')),
            When(account_number__range=("883900", "883999"), then=Value('Саваслейка_GPON')),
            When(account_number__range=("884000", "884299"), then=Value('Останкино')),
            When(account_number__range=("885000", "885499"), then=Value('Чистое Борское')),
            When(account_number__range=("886000", "886399"), then=Value('Дуденево')),
            When(account_number__range=("887000", "887299"), then=Value('Большеорловское')),
            When(account_number__range=("887500", "887899"), then=Value('Лакша')),
            When(account_number__range=("889000", "889099"), then=Value('Юрики')),
            When(account_number__range=("889100", "889299"), then=Value('Боталово')),
            default=Value('Нераспределенные платежи'),
            output_field=CharField(),
        )
    )

    report_data = payments.values('settlement').annotate(total_amount=Sum('amount')).order_by('settlement')

    # Запись результатов в текстовый файл
    with open(report_file_path, 'w') as file:
        for item in report_data:
            line = f"{item['settlement']}: {item['total_amount']}\n"
            file.write(line)


def generate_payment_report(start_date, end_date):
    tinkoff_report_path = 'utils/reports/payment_report_tinkoff.txt'
    sberbank_report_path = 'utils/reports/payment_report_sberbank.txt'

    write_payment_report(PaymentTinkoff, start_date, end_date, tinkoff_report_path)
    write_payment_report(PaymentSberbank, start_date, end_date, sberbank_report_path)
    return tinkoff_report_path, sberbank_report_path
