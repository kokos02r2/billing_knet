import os
import sys

import django
from django.db import transaction

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.abonents.models import Abonent, UserEvent  # noqa


def charge_users():
    with transaction.atomic():  # Начало транзакции
        accounts = Abonent.objects.select_related('login', 'group')
        accounts_to_update = []
        events_to_create = []

        for account in accounts:
            tariff = account.group
            balance = account.balance

            if balance >= 0:
                account.balance -= tariff.month_price
                accounts_to_update.append(account)
                event = UserEvent(
                    abonent=account,
                    event=f"{-tariff.month_price} руб.",
                    comment=f"Снята абонентская плата {tariff.month_price} руб.",
                    new_balance=f"{account.balance} руб."
                )
                events_to_create.append(event)

        if accounts_to_update:
            Abonent.objects.bulk_update(accounts_to_update, ['balance'])
            UserEvent.objects.bulk_create(events_to_create)
            print(f"Updated {len(accounts_to_update)} accounts and created {len(events_to_create)} events.")


if __name__ == '__main__':
    charge_users()
