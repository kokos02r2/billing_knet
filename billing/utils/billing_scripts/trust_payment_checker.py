import os
import sys
import time
from datetime import datetime
from decimal import Decimal

import django
from django.db import DatabaseError, transaction
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(current_dir))

if base_path not in sys.path:
    sys.path.append(base_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.abonents.models import Abonent, UserEvent  # noqa
from utils.telegram_sender import send_telegram_message  # noqa

load_dotenv()


def check_trust_payment():
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            with transaction.atomic():
                accounts = Abonent.objects.select_related('login', 'group').exclude(credit__isnull=True).exclude(credit='')
                accounts_to_update = []
                events_to_create = []

                for account in accounts:
                    current_date = datetime.now()
                    current_month = str(datetime.now().month).zfill(2)
                    date_str, amount_str = account.credit.split('x')
                    credit_date = datetime.strptime(date_str, "%d-%m-%Y")
                    credit_amount = Decimal(amount_str)
                    if credit_date.date() <= current_date.date():
                        account.balance -= credit_amount
                        account.credit = ""
                        account.credit_check = current_month
                        accounts_to_update.append(account)
                        event = UserEvent(
                            abonent=account,
                            event=f"{-credit_amount} руб.",
                            comment=f"Снят доверительный платеж {credit_amount} руб.",
                            new_balance=f"{account.balance} руб."
                        )
                        events_to_create.append(event)
                    else:
                        None
                if accounts_to_update:
                    Abonent.objects.bulk_update(accounts_to_update, ['balance', 'credit', 'credit_check'])
                    UserEvent.objects.bulk_create(events_to_create)
                    print(f"Updated {len(accounts_to_update)} accounts and created {len(events_to_create)} events.")
            break
        except DatabaseError as e:
            handle_error(e, attempt, max_attempts, "Ошибка базы данных при снятии доверительных платежей.")

        except Exception as e:
            handle_error(e, attempt, max_attempts, "Неизвестная ошибка при снятии доверительных платежей.")


def handle_error(e, attempt, max_attempts, error_message):
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    full_error_message = f"{error_message}: {e}"
    print(f"Transaction failed on attempt {attempt + 1} of {max_attempts}: {e}")
    time.sleep(1)
    if attempt + 1 == max_attempts:
        send_telegram_message(bot_token, chat_id, full_error_message)
        raise


if __name__ == '__main__':
    check_trust_payment()
