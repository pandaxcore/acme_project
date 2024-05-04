from django import forms


class BirthdayForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=20)
    last_name = forms.CharField(
        label="Фамилия", help_text="Необязательное поле", required=False
    )
    birtday = forms.DateField(
        label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"})
    )
