import hashlib
import json
import os
import time
from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv

from apps.abonents.models import Abonent, UserEvent
from apps.tinkoff_payments.models import PaymentTinkoff
from apps.tinkoff_payments.payment import TinkoffPaymentInteraction

load_dotenv()

terminal = os.getenv('TERMINAL_ID')
secret_key = os.getenv('TINKOFF_SECRET_KEY')


@csrf_exempt
@require_http_methods(['POST'])
def init_payment(request):
    account = request.POST.get('account')
    total = request.POST.get('total')
    phone = request.POST.get('phone')
    email = request.GET.get('email')
    if not Abonent.objects.filter(account_number=account).exists():
        return JsonResponse({
            'error': 'Аккаунт с таким номером не найден.'
        })
    unique_string = f"{account}{total}{int(time.time())}"
    order_id = hashlib.sha256(unique_string.encode()).hexdigest()[:10]
    tinkoff_payment = TinkoffPaymentInteraction(terminal, secret_key)
    payment_data = {
        "TerminalKey": terminal,
        "Amount": float(total) * 100,
        "OrderId": order_id,
        "Description": f"Платеж на договор {account} сумма {total} руб.",
        "Currency": 643,
        "DATA": {
            "phone": phone,
            "email": email if email else "knets@yandex.ru"
        },
        "Receipt": {
            "Email": email if email else "knets@yandex.ru",
            "Phone": phone,
            "Taxation": "usn_income",
            "Items": [{
                "Name": f"Заказ {order_id}",
                "Price": float(total) * 100,
                "Quantity": 1,
                "Amount": float(total) * 100,
                "Tax": "none"
            }]
        }
    }
    response = tinkoff_payment.init(payment_data)
    if response.get('Success'):
        abonent = Abonent.objects.get(account_number=account)
        PaymentTinkoff.objects.create(
            account=abonent,
            payment_id=response.get('PaymentId'),
            status=response.get('Status'),
            amount=total,
        )
        return JsonResponse({
            'url': response.get('PaymentURL')
        })
    else:
        return JsonResponse({
            'error': 'Произошла ошибка при обработке платежа.'
        })


def init(request):
    return render(request, 'tinkoff/init.html')


@csrf_exempt
@require_http_methods(['POST'])
def recieve_payment(request):
    data = json.loads(request.body.decode('utf-8'))
    payment_id = data.get('PaymentId')
    status = data.get('Status')
    amount = data.get('Amount')
    recieve_token = data.get('Token')
    existing_payment = PaymentTinkoff.objects.filter(payment_id=payment_id).first()
    tinkoff_payment = TinkoffPaymentInteraction(terminal, secret_key)
    token = tinkoff_payment.get_token(request=data)
    if recieve_token == token and existing_payment:
        amount_decimal = Decimal(amount) / 100
        abonent = existing_payment.account
        if status == 'AUTHORIZED' and amount_decimal == existing_payment.amount:
            return HttpResponse('OK', content_type='text/plain')
        if status == 'CONFIRMED' and amount_decimal == existing_payment.amount:
            abonent.balance += amount_decimal
            abonent.save()
            PaymentTinkoff.objects.filter(payment_id=payment_id).update(
                account=abonent,
                status=status,
                stamp=timezone.now()
            )
            UserEvent.objects.create(
                    abonent=abonent,
                    event=f"{amount_decimal} руб.",
                    comment=f"Оплата тинькофф {amount_decimal} руб. id {payment_id}",
                    new_balance=f"{abonent.balance} руб."
                )
            return HttpResponse('OK', content_type='text/plain')
        if status == 'REFUNDED' and amount_decimal == existing_payment.amount:
            abonent.balance -= amount_decimal
            abonent.save()
            PaymentTinkoff.objects.filter(payment_id=payment_id).update(
                account=abonent,
                status=status,
                stamp=timezone.now()
            )
            UserEvent.objects.create(
                    abonent=abonent,
                    event=f"{-amount_decimal} руб.",
                    comment=f"Возврат тинькофф {amount_decimal} руб. id {payment_id}",
                    new_balance=f"{abonent.balance} руб."
                )
            return HttpResponse('OK', content_type='text/plain')
        if status == 'REJECTED' and amount_decimal == existing_payment.amount:
            PaymentTinkoff.objects.filter(payment_id=payment_id).update(
                account=abonent,
                status=status,
                stamp=timezone.now()
            )
            return HttpResponse('OK', content_type='text/plain')
    return HttpResponse('Payment not confirmed or not found', content_type='text/plain', status=400)
