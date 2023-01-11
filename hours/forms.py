from django import forms


class CalculateForm(forms.Form):
    up_file = forms.FileField(label="Arquivo")
