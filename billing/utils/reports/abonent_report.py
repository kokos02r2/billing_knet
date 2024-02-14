import os
import sys
from django.db.models import Case, When, CharField, Value, Count, Q
import django
from django.utils import timezone

# Установка путей и Django окружения
current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))
if base_path not in sys.path:
    sys.path.append(base_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.abonents.models import Abonent



def write_subscriber_count_report(model, report_file_path):
    now = timezone.localtime(timezone.now()).strftime("%d.%m.%Y %H:%M:%S")
    abonents = model.objects.annotate(
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
            default=Value('Нераспределенные'),
            output_field=CharField(),
        )
    ).values('settlement').annotate(
        positive_count=Count('id', filter=Q(balance__gte=0)),
        negative_count=Count('id', filter=Q(balance__lt=0))
    ).order_by('settlement')

    total_positive = model.objects.filter(balance__gte=0).count()
    total_negative = model.objects.filter(balance__lt=0).count()
    total_abonents = model.objects.count()

    # Запись результатов в текстовый файл
    with open(report_file_path, 'w') as file:
        file.write(f"Дата и время формирования отчета: {now}\n\n")  # Запись даты и времени в начало файла
        for item in abonents:
            file.write(f"{item['settlement']}:\n {item['positive_count']} абонентов с положительным балансом,\n {item['negative_count']} абонентов с отрицательным балансом\n\n")
        # Вывод общего итога
        file.write("\nОбщее количество абонентов: {}\n".format(total_abonents))
        file.write("С положительным балансом: {}\n".format(total_positive))
        file.write("С отрицательным балансом: {}\n".format(total_negative))


def generate_subscriber_count_report():
    report_file_path = '/home/kokos/billing_knet/billing/utils/reports/subscriber_count_report.txt'
    write_subscriber_count_report(Abonent, report_file_path)
    return report_file_path


if __name__ == '__main__':
    generate_subscriber_count_report()
