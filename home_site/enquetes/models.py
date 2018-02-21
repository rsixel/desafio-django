from django.db import models


class Enquete(models.Model):
    texto = models.CharField(max_length=250)


class Resposta(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    opcao = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
