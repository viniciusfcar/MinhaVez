from django import forms
from .models import Fila

class FormFila(forms.ModelForm):
    class Meta:
        model = Fila
        fields = ['nome', 'vagas']