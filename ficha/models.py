from django.db import models
from usuario.models import Usuario


class Ficha(models.Model):
    numero = models.IntegerField(blank=False, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    preferencial = models.BooleanField()
    status = models.CharField(max_length=20)
    excluida = models.BooleanField()

    def __int__(self):
        return self.usuario.user.username