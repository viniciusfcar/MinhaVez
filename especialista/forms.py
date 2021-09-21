from django.forms import ModelForm
from .models import Especialista
from django.contrib.auth.models import User

class FormEspecialista(ModelForm):
    class Meta:
        model = Especialista
        fields = ['nome', 'sobrenome', 'profissao', 'imagem']