from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Juegos
from django.http import HttpResponseForbidden

# Página principal: solo reseñas
class HomeView(ListView):
    model = Juegos
    template_name = 'blog/home.html'
    context_object_name = 'juegos'

    def get_queryset(self):
        return Juegos.objects.filter(es_reseña=True)

# Lista completa de reseñas
class ListaJuegosView(ListView):
    model = Juegos
    template_name = 'blog/lista_juegos.html'
    context_object_name = 'juegos'

    def get_queryset(self):
        return Juegos.objects.filter(es_reseña=True)

# Vista de detalle de un juego
class JuegoDetailView(DetailView):
    model = Juegos
    template_name = 'blog/juegos_detalle.html'
    context_object_name = 'juego'

# Vista de juegos descargables (con archivo)
class DescargaJuegosView(ListView):
    model = Juegos
    template_name = 'blog/descargar_juegos.html'
    context_object_name = 'juegos'

    def get_queryset(self):
        return Juegos.objects.exclude(archivo='')

# Vista para subir juegos descargables (solo staff/admin)
class SubirJuegoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Juegos
    template_name = 'blog/subir_juegos.html'
    fields = ['titulo', 'autor', 'categoria', 'descripcion', 'imagen', 'archivo']
    success_url = reverse_lazy('descargar_juegos')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseForbidden("No tenés permiso para acceder a esta página.")

# Vista para crear reseñas (sin archivo)
class CrearReseñaView(LoginRequiredMixin, CreateView):
    model = Juegos
    template_name = 'blog/crear_reseña.html'
    fields = ['titulo', 'autor', 'categoria', 'descripcion', 'imagen']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.archivo = None
        form.instance.es_reseña = True  # ✅ marcar como reseña
        return super().form_valid(form)



