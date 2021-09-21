from rest_framework import serializers
from .models import Fila

class FilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fila
        fields = ('id', 'nome', 'vagas', 'fila_preferencial', 'fichas', 'total_fichas')