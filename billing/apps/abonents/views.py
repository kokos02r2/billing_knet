import os
import zipfile

from django.shortcuts import render
from django.http import HttpResponse
from .forms import DateRangeForm
from utils.reports.money_report import generate_payment_report
from django.contrib.admin.views.decorators import staff_member_required
from io import BytesIO


@staff_member_required
def report_view(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            tinkoff_report_path, sberbank_report_path = generate_payment_report(start_date, end_date)

            # Создаем архив в памяти
            response = HttpResponse(content_type='application/zip')
            zip_file = BytesIO()
            with zipfile.ZipFile(zip_file, 'w') as zf:
                zf.write(tinkoff_report_path, arcname=os.path.basename(tinkoff_report_path))
                zf.write(sberbank_report_path, arcname=os.path.basename(sberbank_report_path))
            zip_file.seek(0)

            # Устанавливаем заголовок для скачивания файла
            response['Content-Disposition'] = 'attachment; filename="reports.zip"'
            response.write(zip_file.read())
            return response
    else:
        form = DateRangeForm()
    return render(request, 'admin/payment_report.html', {'form': form})
