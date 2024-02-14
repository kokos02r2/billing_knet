from django import forms


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'Выберите дату'}),
    )
    end_date = forms.DateField(
        label='Дата окончания',
        widget=forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'Выберите дату'}),
    )
