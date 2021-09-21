from django import forms
from .models import Ficha

class FormFicha(forms.ModelForm):
    class Meta:
        model = Ficha
        fields = ['preferencial',]