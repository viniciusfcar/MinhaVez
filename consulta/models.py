from django.db import models
from agendamento.models import Agendamento
from especialista.models import Especialista
from fila.models import Fila
from django.contrib.auth.models import User

class Consulta(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    especialista = models.ForeignKey(Especialista, on_delete=models.SET_NULL, related_name='consultas', null=True, blank=False)
    data = models.DateField(auto_now=False, auto_now_add=False)
    filas = models.ManyToManyField(Fila, blank=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    create_fila = models.BooleanField()
    status = models.CharField(max_length=10)
    hora = models.CharField(max_length=5, blank=False)

    #serve para ver se existe agendamento para a autorização
    verifica = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


