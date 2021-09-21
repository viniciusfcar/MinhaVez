from django.db import models
from responsavel.models import Responsavel
from agendamento.models import Agendamento
from fila.models import Fila
from django.contrib.auth.models import User

class Autorizacao(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=False)
    data = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    filas = models.ManyToManyField(Fila, blank=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_fila = models.BooleanField()
    status = models.CharField(max_length=10)
    hora = models.CharField(max_length=5, blank=False)

    #serve para ver se existe agendamento para a autorização
    verifica = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


