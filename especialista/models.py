from django.db import models
from profissao.models import Profissao
from especializacao.models import Especializacao

class Especialista(models.Model):

    nome = models.CharField(max_length=20, blank=False)
    sobrenome = models.CharField(max_length=20, blank=False)
    profissao = models.ForeignKey(Profissao, on_delete=models.SET_NULL, null=True, blank=False)
    especializacao = models.ManyToManyField(Especializacao, blank=False)
    num_conselho = models.CharField(max_length=100, blank=False)
    conselho = models.CharField(max_length=20, blank=False)
    estado_conselho = models.CharField(max_length=2, blank=False)
    imagem = models.ImageField(upload_to='fotos_especialistas', null=False, blank=False)
    

    def __str__(self):
        return self.nome + ' - ' + self.profissao.nome
