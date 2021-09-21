from django.forms import ModelForm
from .models import Responsavel

class FormResponsavel(ModelForm):
    class Meta:
        model = Responsavel
        fields = ['imagem', 'nome', 'sobrenome']