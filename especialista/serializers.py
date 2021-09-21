from rest_framework import serializers
from .models import Especialista

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = ('id', 'nome', 'sobrenome', 'profissao', 'especializacao', 'imagem')