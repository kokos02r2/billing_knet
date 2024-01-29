import calendar
from datetime import datetime, timedelta

from apps.abonents.event_writer import write_event_trust


def set_trust_payment(abonent):
    current_month = datetime.now().strftime("%m")
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
                abonent.credit = f"{formatted_date}x{trust_payment}"
                abonent.credit_check = f"{current_month}"
                abonent.save()
                return (f"Доверительный платеж на сумму {trust_payment} руб. до {formatted_date} успешно оформлен")
            else:
                trust_payment = - abonent.balance
                abonent.balance += - abonent.balance
                abonent.credit = f"{formatted_date}x{trust_payment}"
                abonent.credit_check = f"{current_month}"
                write_event_trust(abonent, trust_payment, abonent.balance)
                abonent.save()
                return (f"Доверительный платеж на сумму {trust_payment} руб. до {formatted_date} успешно оформлен")
        else:
            if abonent.balance < abonent.group.month_price:
                future_date = datetime.now() + timedelta(days=5)
                formatted_date = future_date.strftime("%d-%m-%Y")
                new_balance = abonent.group.month_price
                trust_payment = new_balance - abonent.balance
                abonent.credit = f"{formatted_date}x{trust_payment}"
                abonent.credit_check = f"{current_month}"
                abonent.balance = new_balance
                write_event_trust(abonent, trust_payment, abonent.balance)
                abonent.save()
                return (f"Доверительный платеж на сумму {trust_payment} руб. до {formatted_date} успешно оформлен")
            else:
                return ("Денег достаточно доверительный не нужен")
