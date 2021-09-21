from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'user', 'cpf', 'rg', 'sus', 'cep', 'logradouro', 'numero',
                  'complemento', 'bairro', 'cidade', 'estado', 'telefone', 'sexo', 'notificacao', 'imagem',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('imagem', )