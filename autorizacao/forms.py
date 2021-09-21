from django import forms
from .models import Autorizacao

class FormAutorizacao(forms.ModelForm):
    class Meta:
        model = Autorizacao
        fields = ['nome', 'responsavel', 'data',]

class FormModalAutorizacao(forms.Form):
    cpf = forms.CharField(max_length=11)