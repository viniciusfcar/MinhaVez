from rest_framework import serializers
from .models import Profissao

class ProfissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissao
        fields = ('id', 'nome',)