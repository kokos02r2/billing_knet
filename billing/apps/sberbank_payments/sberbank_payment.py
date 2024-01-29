import re
from datetime import datetime

from django.http import HttpResponse


class SberbankPaymentInteraction:
    @staticmethod
    def generate_response(txn_id, result, comment):
        xml_response = f'<?xml version="1.0" encoding="windows-1251"?>' \
                       f'<response>' \
                       f'<txn_id>{txn_id}</txn_id>' \
                       f'<result>{result}</result>' \
                       f'<comment>{comment}</comment>' \
                       f'</response>'
        xml_response_encoded = xml_response.encode('cp1251')
        return HttpResponse(xml_response_encoded, content_type='application/xml')

    @staticmethod
    def process_request(request):
        data = request.GET
        if not data.get('txn_id'):
            return SberbankPaymentInteraction.generate_response("", 1, 'Не указан параметр txn_id', True)
        command = data.get('command')
        txn_id = data.get('txn_id')
        if not command:
            return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Не указан параметр command', True)
        if command not in ['check', 'pay']:
            return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Некорректный параметр command: ' + command, True)

        account = data.get('account')
        if not account:
            return SberbankPaymentInteraction.generate_response(txn_id, 4, 'Не указан параметр account', True)
        if not re.match(r'^\d{6,}$', account):
            return SberbankPaymentInteraction.generate_response(txn_id, 4, 'Некорректный параметр account: ' + account, True)

        if command == 'pay':
            sum_ = data.get('sum')
            if not sum_:
                return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Не указан параметр sum', True)
            if not re.match(r'^\d+(\.\d+)?$', sum_):
                return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Некорректный параметр sum: ' + sum_, True)

            if not re.match(r'^\d{1,20}$', txn_id):
                return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Некорректный параметр txn_id: ' + txn_id, True)

            txn_date = data.get('txn_date')
            if not txn_date:
                return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Не указан параметр txn_date', True)
            if not re.match(r'^\d{14}$', txn_date):
                return SberbankPaymentInteraction.generate_response(txn_id, 1, 'Некорректный параметр txn_date: ' + txn_date, True)

        return None

    @staticmethod
    def parse_txn_date(txn_date_str):
        return datetime.strptime(txn_date_str, '%Y%m%d%H%M%S')
