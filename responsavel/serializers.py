from rest_framework import serializers
from .models import Responsavel

class ReponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ('id', 'nome', 'sobrenome', 'imagem')