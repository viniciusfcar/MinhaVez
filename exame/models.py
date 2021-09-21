from django.db import models
from fila.models import Fila
from agendamento.models import Agendamento
from django.contrib.auth.models import User 

class Exame(models.Model):

    TIPO_CHOICES = (
        ("Urina", "URINA"),
        ("Sangue", "SANGUE"),
        ("Fezes", "FEZES"),
        ("Radiológico", "RADIOLÓGICO"),
        ("Elétrico", "ELÉTRICO"),
        ("Ultrassonografia", "ULTRASSONOGRAFIA"),
    )

    nome = models.CharField(max_length=100, blank=False)
    data = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    filas = models.ManyToManyField(Fila, blank=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_fila = models.BooleanField()
    status = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=False, null=False)
    hora = models.CharField(max_length=5, blank=False)

    #serve para ver se existe agendamento para o exame
    verifica = models.BooleanField(default=False)

    def __str__(self):
        return self.tipo + self.nome