from django import forms
from .models import Consulta

class FormConsulta(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nome', 'especialista', 'data',]

class FormModalConsulta(forms.Form):
    cpf = forms.CharField(max_length=11)