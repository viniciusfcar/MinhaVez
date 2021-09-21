from rest_framework import serializers
from .models import Autorizacao

class AutorizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autorizacao
        fields = ('id', 'nome', 'responsavel', 'status', 'data', 'hora', 'filas', 'agendamento', 'create_fila')