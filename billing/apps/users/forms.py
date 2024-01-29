from django import forms


class ChangeTarifContactForm(forms.Form):

    tarif = forms.ChoiceField(label='Выберите новый тариф')

    def __init__(self, *args, **kwargs):
        account_number = kwargs.pop('account_number', None)
        super(ChangeTarifContactForm, self).__init__(*args, **kwargs)

        if account_number and account_number.startswith('883'):
            choices = [
                ('Econom (650 руб.) 25 Мбит/c', 'Econom (650 руб.) 25 Мбит/c'),
                ('Optimum (850 руб.) 50 Мбит/c', 'Optimum (850 руб.) 50 Мбит/c'),
                ('Maximum (1050 руб.) 100 Мбит/c', 'Maximum (1050 руб.) 100 Мбит/c'),
                ('EconomGPON+TV', 'Econom+TV (800 руб.) 25 Мбит/c'),
                ('Econom+TV (800 руб.) 25 Мбит/c', 'Optimum+TV (1000 руб.) 50 Мбит/c'),
                ('Maximum+TV (1200 руб.) 100 Мбит/c', 'Maximum+TV (1200 руб.) 100 Мбит/c')
            ]
        else:
            choices = [
                ('Econom (350 руб.) 25 Мбит/c', 'Econom (350 руб.) 25 Мбит/c'),
                ('Optimum (450 руб.) 50 Мбит/c', 'Optimum (450 руб.) 50 Мбит/c'),
                ('Maximum (550 руб.) 100 Мбит/c', 'Maximum (550 руб.) 100 Мбит/c'),
                ('Econom+TV (500 руб.) 25 Мбит/c', 'Econom+TV (500 руб.) 25 Мбит/c'),
                ('Optimum+TV (600 руб.) 50 Мбит/c', 'Optimum+TV (600 руб.) 50 Мбит/c'),
                ('Maximum+TV (700 руб.) 100 Мбит/c', 'Maximum+TV (700 руб.) 100 Мбит/c')
            ]

        self.fields['tarif'].choices = choices


class ChangeStatusContactForm(forms.Form):
    STATUS_CHOICES = [
        ('Заблокировать', 'Заблокировать'),
        ('Разблокировать', 'Разблокировать')
    ]
    block_status = forms.ChoiceField(choices=STATUS_CHOICES, label='Выберите действие')
