from django.urls import path
from .views import (
    HomeView,
    ListaJuegosView,
    JuegoDetailView,
    DescargaJuegosView,
    SubirJuegoView,
    CrearReseñaView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', ListaJuegosView.as_view(), name='lista_juegos'),
    path('juego/<int:pk>/', JuegoDetailView.as_view(), name='juego_detalle'),  # 👈 ESTA ES LA CLAVE
    path('descargar/', DescargaJuegosView.as_view(), name='descargar_juegos'),
    path('subir-juego/', SubirJuegoView.as_view(), name='subir_juego'),
    path('crear-resena/', CrearReseñaView.as_view(), name='crear_resena'),
]

