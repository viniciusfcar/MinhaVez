from django import forms
from .models import Agendamento

class FormAgendamento(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['nome',]

class FormModalAgendamento(forms.Form):
    cpf = forms.CharField(max_length=11)