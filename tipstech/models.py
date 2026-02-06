from django.db import models

class Dicas(models.Model):
    titulo = models.CharField(max_length=100, null= False, blank=False)
    descricao = models.TextField(null= False, blank=False)
