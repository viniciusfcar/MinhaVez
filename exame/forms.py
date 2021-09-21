from django import forms
from .models import Exame

class FormExame(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['tipo', 'nome', 'data']