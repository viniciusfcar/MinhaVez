from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EspecializacaoSerializer
from .models import Especializacao
import json
from django.core import serializers
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
import json

class GetEspecializacaoViewSet(viewsets.ModelViewSet):
    serializer_class = EspecializacaoSerializer    
    filter_backends = (SearchFilter,)
    search_fields = ['^nome']

    def get_queryset(self):
        queryset = Especializacao.objects.all()
        return queryset
    
