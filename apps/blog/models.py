from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre
    
# Clase juegos == Post
class Juegos(models.Model):
    titulo = models.CharField(max_length=45, null=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='juegos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    fecha_agregado = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='libros',
                            null=True,
                            blank=True,
                            default='img/img_post_default.jpg')
    archivo = models.FileField(upload_to='juegos/', null=True, blank=True)
# Muestra como se representa en la lista de libros

    es_reseña = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo