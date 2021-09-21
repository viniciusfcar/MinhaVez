from django.db import models

class Notificacao(models.Model):

    titulo = models.CharField(max_length=50, blank=False, null=False)
    assunto = models.CharField(max_length=300, blank=False, null=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo