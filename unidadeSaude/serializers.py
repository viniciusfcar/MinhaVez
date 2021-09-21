from rest_framework import serializers
from .models import UnidadeSaude

class UnidadeSaudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeSaude
        fields = ('id', 'razao_social', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
                  'consultas', 'autorizacoes', 'especialistas', 'exames', 'responsaveis', 'telefone', 'email')