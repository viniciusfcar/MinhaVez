from rest_framework import serializers
from .models import Especializacao

class EspecializacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especializacao
        fields = ('id', 'nome',)