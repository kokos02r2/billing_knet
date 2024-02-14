from apps.groups.models import Group
from apps.abonents.models import UserEvent

from core.helpers.сhange_tarif import get_days_left_in_month


def recalculation_logic(abonent, days):
    _, days_in_month = get_days_left_in_month()
    group = Group.objects.get(group_name=abonent.group)
    add_amount = round((group.month_price / days_in_month) * days)
    abonent.balance += add_amount
    abonent.save()
    event = UserEvent(
        abonent=abonent,
        event=f"{add_amount} руб.",
        comment=f"Перерасчет {add_amount} руб.",
        new_balance=f"{abonent.balance} руб."
    )
    event.save()
    return (f"Произведен перерасчет на сумму {add_amount} руб. для договора {abonent.account_number}")
