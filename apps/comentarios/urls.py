from django.urls import path
from .views import agregar_comentario, listar_comentarios, ModificarComentario, EliminarComentario

app_name = 'apps.comentarios'

urlpatterns = [
    path('agregar_comentario/<int:juego_id>/', agregar_comentario, name = 'agregar_comentario'),
    path('comentarios/', listar_comentarios, name = 'comentarios'),
    path('modificar_comentario/<int:pk>', ModificarComentario.as_view(), name= 'modificar_comentario'),
    path('eliminar_comentario/<int:pk>', EliminarComentario.as_view(), name= 'eliminar_comentario'),
    
]