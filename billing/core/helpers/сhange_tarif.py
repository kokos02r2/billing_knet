from datetime import datetime
import calendar

from apps.abonents.models import UserEvent
from apps.groups.models import Group

from core.helpers.ip_generator_from_pool import generate_unique_ip_from_range
from core.helpers.ip_generator_unique import generate_unique_ip
from core.helpers.constants import CONTRACT_RANGES


def get_days_left_in_month():
    current_date = datetime.now()
    first_day_of_next_month = current_date.replace(day=1, month=current_date.month + 1)
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    if current_date.month == 12:
        first_day_of_next_month = first_day_of_next_month.replace(year=current_date.year + 1, month=1)
    days_left_in_month = (first_day_of_next_month - current_date).days
    return days_left_in_month, days_in_month


def change_tarif_logic(abonent, new_tariff):
    days_left_in_month, days_in_month = get_days_left_in_month()
    current_group = abonent.group
    month_price_old = current_group.month_price
    old_tariff = abonent.group
    new_group = Group.objects.get(group_name=new_tariff)
    month_price_new = new_group.month_price
    if any(start <= int(abonent.account_number) <= end for start, end in CONTRACT_RANGES):
        new_ip_address = generate_unique_ip()
    else:
        new_ip_address = generate_unique_ip_from_range(str(new_tariff), int(abonent.account_number))
    if month_price_new > month_price_old:
        new_balance = abonent.balance - round(((month_price_new - month_price_old) / days_in_month) * days_left_in_month)
    elif month_price_new < month_price_old:
        new_balance = abonent.balance + round(((month_price_old - month_price_new) / days_in_month) * days_left_in_month)
    else:
        new_balance = abonent.balance
    if "TV" in str(new_tariff):
        email = str(abonent.account_number) + '@knet-nn.ru'
    else:
        email = ''
    abonent.email = email
    abonent.balance = new_balance
    abonent.ip_addr = new_ip_address
    abonent.group = new_group
    abonent.save()
    event = UserEvent(
        abonent=abonent,
        event=f"Старый тариф {old_tariff}",
        comment=f"Изменение тарифа на {new_tariff}",
        new_balance=f"{abonent.balance} руб."
    )
    event.save()
