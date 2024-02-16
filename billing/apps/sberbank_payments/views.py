import logging
from decimal import Decimal

from django.views.decorators.http import require_http_methods

from apps.abonents.models import Abonent, UserEvent
from apps.sberbank_payments.models import PaymentSberbank
from django.db import transaction

from .decorators import basic_auth_required
from .sberbank_payment import SberbankPaymentInteraction

logger = logging.getLogger('sberbank')


@basic_auth_required
@require_http_methods(['GET'])
def recieve_payment_sberbank(request):
    try:
        error_response = SberbankPaymentInteraction.process_request(request)
        if error_response:
            return error_response
        status = request.GET.get('command')
        txn_id = request.GET.get('txn_id')
        amount = request.GET.get('sum')
        account = request.GET.get('account')
        remote_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')
        message = f"{account} {amount} {txn_id}"
        response_ok = SberbankPaymentInteraction.generate_response(txn_id, 0, 'OK')
        with transaction.atomic():
            if status == 'check':
                if not Abonent.objects.filter(account_number=account).exists():
                    message = f"{account} {amount} {txn_id} {remote_addr}: Аккаунт с таким номером не найден"
                    logger.info(message)
                    return SberbankPaymentInteraction.generate_response(
                        txn_id, 5, 'Аккаунт с таким номером не найден'
                    )
                else:
                    message = f"{account} {amount} {txn_id} {remote_addr}: check успешно"
                    logger.info(message)
                    return response_ok

            if status == 'pay':
                if Abonent.objects.filter(account_number=account).exists():
                    if PaymentSberbank.objects.filter(txn_id=txn_id).exists():
                        message = f"{account} {amount} {txn_id} {remote_addr}: Такой ID платежа уе есть в базе"
                        logger.info(message)
                        return response_ok
                    else:
                        txn_date_str = request.GET.get('txn_date')
                        abonent = Abonent.objects.get(account_number=account)
                        PaymentSberbank.objects.create(
                            account=abonent,
                            account_number=account,
                            txn_id=txn_id,
                            status=status,
                            amount=amount,
                            txn_date=SberbankPaymentInteraction.parse_txn_date(txn_date_str)
                        )
                        abonent.balance += Decimal(amount)
                        abonent.save()
                        UserEvent.objects.create(
                            abonent=abonent,
                            event=f"{amount} руб.",
                            comment=f"Оплата Сбербанк {amount} руб. id {txn_id}",
                            new_balance=f"{abonent.balance} руб."
                        )
                        message = f"{account} {amount} {txn_id} {remote_addr}: Платеж проведен успешно"
                        logger.info(message)
                        return response_ok
                message = f"{account} {amount} {txn_id} {remote_addr}: Ошибка биллинга"
                logger.info(message)
                return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Ошибка биллинга')
    except Exception as e:
        message = f"Неожиданная ошибка: {e} | IP: {request.META.get('REMOTE_ADDR', '127.0.0.1')}"
        logger.error(message)
        return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Внутренняя ошибка сервера')
