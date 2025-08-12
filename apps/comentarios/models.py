from django.db import models
from apps.blog.models import Juegos
from apps.login.models import PerfilUsuario

# Create your models here.

class Comentario(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    blog = models.ForeignKey(Juegos, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField(verbose_name='Comentario')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto
    
    class Meta:
        ordering = ['-fecha',]