from django.contrib.auth.models import User
from django.db import models

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    imagen = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"