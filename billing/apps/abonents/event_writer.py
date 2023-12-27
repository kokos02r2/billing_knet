from .models import UserEvent


def write_event_trust(abonent, trust_payment, new_balance):
    event_for_writing = [UserEvent(
                abonent=abonent,
                event=f"{trust_payment} руб.",
                comment=f"Взят доверительный Админ на сумму {trust_payment} руб.",
                new_balance=f"{new_balance} руб."
            )]
    UserEvent.objects.bulk_create(event_for_writing)
