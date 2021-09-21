from django.db import models
from ficha.models import Ficha

class Fila(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    fichas = models.ManyToManyField(Ficha, blank=False)
    vagas = models.IntegerField(blank=False, null=False)
    fila_preferencial = models.BooleanField()
    total_fichas = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=10)


    def __str__(self):
        return self.nome