from django import forms
from .models import Usuario
from django.contrib.auth.models import User

class FormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['sexo', 'imagem']

class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']