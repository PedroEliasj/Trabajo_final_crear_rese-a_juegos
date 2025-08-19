from django.urls import path

from .views import (
    HomeView,
    ListaJuegosView,
    JuegoDetailView,
    DescargaJuegosView,
    SubirJuegoView,
    CrearReseñaView,
    EditarReseñaView,
    EliminarReseñaView,
    blog
)
from apps.blog import views
app_name = 'apps.blog'


urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('blog/', blog.as_view(), name='blog'),
    path('lista_juegos/', ListaJuegosView.as_view(), name='lista_juegos'),
    path('juego/<int:id>/', JuegoDetailView, name='juego_detalle'),  
    path('descargar/', DescargaJuegosView.as_view(), name='descargar_juegos'),
    path('subir-juego/', SubirJuegoView.as_view(), name='subir_juego'),
    path('crear-resena/', CrearReseñaView.as_view(), name='crear_resena'),
    path('post/<int:pk>/editar/', EditarReseñaView.as_view(), name='editar_post'),
    path('post/<int:pk>/eliminar/', EliminarReseñaView.as_view(), name='eliminar_post'),
    path("like/<int:juego_id>/", views.like_post, name="like_post"),
]