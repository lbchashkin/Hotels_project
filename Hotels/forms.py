from django import forms

from .models import Filials, Guests


class GuestForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    class Meta:
        model = Guests
        fields = ['g_name', 'g_gender', 'g_born', 'g_phone', 'g_mail', 'g_passp']


class FindEmptyRoomsForm(forms.Form):
    filial = forms.ChoiceField(label='Филиал', choices=[(filial.f_id, filial) for filial in Filials.objects.all()])
    arrival_date = forms.DateField(label='Дата заезда', widget=forms.SelectDateWidget())
    departure_date = forms.DateField(label='Дата выезда', widget=forms.SelectDateWidget())
