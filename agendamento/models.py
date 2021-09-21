from django.db import models
from usuario.models import Usuario

class Agendamento(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    usuarios = models.ManyToManyField(Usuario, blank=True)
    escolha = models.BooleanField(default=False)
    vagas = models.IntegerField()

    #Esse participar é permitir que o úsuario possa participar da fila
    participar = models.BooleanField(default=False)


    def __str__(self):
        return self.nome


