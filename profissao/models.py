from django.db import models

class Profissao(models.Model):
    nome = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.nome
