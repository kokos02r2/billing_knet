from django.conf import settings

from django.core.mail import send_mail


def send_abonent_mail(abonent, tarif, subject):
    full_message = f"""
    Имя: {abonent.name}
    Номер договора: {abonent.account_number}
    Тариф: {tarif}
    """
    email_theme = f'{subject} договор {abonent.account_number}'
    send_mail(
        email_theme,
        full_message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_ADDRESS],
        fail_silently=False,
    )
