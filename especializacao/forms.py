from django.forms import ModelForm
from .models import Especializacao

class FormEspecializacao(ModelForm):
    class Meta:
        model = Especializacao
        fields = ['nome']