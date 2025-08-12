from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from apps.comentarios.forms import ComentarioForm
from apps.comentarios.models import Comentario
from apps.login.models import PerfilUsuario
from .models import Juegos
from django.http import HttpResponseForbidden


# Página principal: solo reseñas
# class HomeView(ListView):
#     model = Juegos
#     template_name = 'blog/home.html'
#     context_object_name = 'juegos'

#     def get_queryset(self):
#         return Juegos.objects.filter(es_reseña=True)

class HomeView(ListView):
    model = Juegos
    template_name = 'blog/home.html'
    context_object_name = 'juegos'

    def get_queryset(self):
        return Juegos.objects.filter(es_reseña=True).prefetch_related('comentarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['perfil'] = PerfilUsuario.objects.get(user=self.request.user)
            except PerfilUsuario.DoesNotExist:
                context['perfil'] = None
        return context

# Lista completa de reseñas
class ListaJuegosView(ListView):
    model = Juegos
    template_name = 'blog/lista_juegos.html'
    context_object_name = 'juegos'

    def get_queryset(self):
        return Juegos.objects.filter(es_reseña=True)

# Vista de detalle de un juego
# class JuegoDetailView(DetailView):
#     model = Juegos
#     template_name = 'blog/juegos_detalle.html'
#     context_object_name = 'juego'
def JuegoDetailView(request, id):
    juego = Juegos.objects.get(id = id)
    comentarios = Comentario.objects.filter(blog=juego)
    form = ComentarioForm(request.POST)
    
    if form.is_valid():
        if request.user.is_authenticated:
            aux = form.save(commit=False)
            aux.blog = juego
            perfil = PerfilUsuario.objects.get(user=request.user)
            aux.usuario = perfil
            aux.save()
            form = ComentarioForm()
        else:
            return redirect('apps.usuarios:iniciar_sesion')
    context={
        'juego' : juego,
        'form' : form,
        'comentarios' : comentarios
    }
    return render(request, 'blog/juegos_detalle.html', context)

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
    fields = ['titulo', 'categoria', 'descripcion', 'imagen']
    success_url = reverse_lazy('apps.blog:home')

    def form_valid(self, form):
                # DEBUG para ver si entra acá y si hay usuario
        # print("====== DEBUG CREAR RESEÑA ======")
        # print("Usuario logueado:", self.request.user)
        # print("¿Está autenticado?:", self.request.user.is_authenticated)
        # print("Tipo de usuario:", type(self.request.user))


        form.instance.autor = self.request.user  # 🔹 asignar autor logueado
        form.instance.archivo = None
        form.instance.es_reseña = True  # ✅ marcar como reseña
        return super().form_valid(form)

