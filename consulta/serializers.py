from rest_framework import serializers
from .models import Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ('id', 'nome', 'especialista', 'data', 'hora', 'filas', 'status', 'agendamento', 'create_fila')