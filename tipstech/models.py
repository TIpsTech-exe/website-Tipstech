from django.db import models

class Comentarios(models.Model):
    nome = models.CharField(max_length=100, null= False, blank=False)
    comentado = models.TextField(null= False, blank=False)
    data_da_postagem = models.DateTimeField(auto_now_add=True)
    qtd_likes = models.IntegerField(default=0)
