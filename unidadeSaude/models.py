from django.db import models
from django.contrib.auth.models import User
from consulta.models import Consulta
from autorizacao.models import Autorizacao
from especialista.models import Especialista
from responsavel.models import Responsavel
from exame.models import Exame

class UnidadeSaude(models.Model):

    users = models.ManyToManyField(User, blank=True)
    razao_social = models.CharField(max_length=100, blank=False, null=False)
    cnpj = models.CharField(max_length=18, blank=False, unique=True)
    logradouro = models.CharField(max_length=50, blank=False, unique=False)
    numero = models.IntegerField(blank=False, unique=False)
    complemento = models.CharField(max_length=50, blank=True, unique=False)
    bairro = models.CharField(max_length=50, blank=False, unique=False)
    cidade = models.CharField(max_length=50, blank=False, unique=False)
    estado = models.CharField(max_length=2, blank=False, unique=False)
    consultas = models.ManyToManyField(Consulta, blank=True)
    autorizacoes = models.ManyToManyField(Autorizacao, blank=True)
    especialistas = models.ManyToManyField(Especialista, blank=True,)
    responsaveis = models.ManyToManyField(Responsavel, blank=True)
    exames = models.ManyToManyField(Exame, blank=True)
    telefone = models.CharField(max_length=15, blank=False, null=True)
    email = models.EmailField(max_length=100, blank=False, null=True)
    cep = models.CharField(max_length=9, blank=False, null=False)

    def __str__(self):
        return self.razao_social


