from django.forms import ModelForm
from .models import Profissao

class FormProfissao(ModelForm):
    class Meta:
        model = Profissao
        fields = ['nome']