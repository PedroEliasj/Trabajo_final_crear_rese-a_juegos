from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from apps.blog.forms import PostForm
from apps.comentarios.forms import ComentarioForm
from apps.comentarios.models import Comentario
from apps.login.models import PerfilUsuario
from .models import Categoria, Juegos
from django.http import HttpResponseForbidden, JsonResponse

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

import sys

class HomeView(ListView):
    model = Juegos
    template_name = 'blog/index.html'
    context_object_name = 'juegos'

class blog(ListView):
    model = Juegos
    template_name = 'blog/blog.html'
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
                
        # Traer solo las categorías que están asociadas a reseñas
        context['categorias'] = Categoria.objects.filter(
            juegos__es_reseña=True
        ).distinct().order_by('nombre')
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
    form_class = PostForm
    template_name = 'blog/crear_post.html'
    # fields = ['titulo', 'categoria', 'descripcion', 'imagen']
    success_url = reverse_lazy('apps.blog:blog')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].required = False
        return form

    def form_valid(self, form):
        nueva_categoria = self.request.POST.get('nueva_categoria', '').strip()

        if nueva_categoria:
            categoria_obj, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
            form.instance.categoria = categoria_obj
        else:
            # Si no se eligió nueva categoría ni del select
            if not form.cleaned_data.get('categoria'):
                form.add_error('categoria', 'Debes seleccionar o crear una categoría.')
                return self.form_invalid(form)

        form.instance.autor = self.request.user  # 🔹 asignar autor logueado
        form.instance.archivo = None
        form.instance.es_reseña = True  # ✅ marcar como reseña
        return super().form_valid(form)
    
    # para mostrar foto de perfil
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = None
        if self.request.user.is_authenticated:
            perfil = get_object_or_404(PerfilUsuario, user=self.request.user)
        context['perfil'] = perfil
        return context

class EditarReseñaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Juegos
    form_class = PostForm
    template_name = 'blog/editar_post.html'
    success_url = reverse_lazy('apps.blog:blog')

    def test_func(self):
        """El autor o un staff pueden editar"""
        juego = self.get_object()
        return juego.autor == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        form.instance.es_reseña = True  # aseguramos que siga marcado como reseña
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = None
        if self.request.user.is_authenticated:
            try:
                perfil = PerfilUsuario.objects.get(user=self.request.user)
            except PerfilUsuario.DoesNotExist:
                perfil = None
        context['perfil'] = perfil
        return context
    
class EliminarReseñaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Juegos
    template_name = 'blog/eliminar_post.html'
    success_url = reverse_lazy('apps.blog:blog')

    def test_func(self):
        """El autor o un staff pueden eliminar"""
        juego = self.get_object()
        return juego.autor == self.request.user or self.request.user.is_staff

@login_required
def like_post(request, juego_id):

    juego = get_object_or_404(Juegos, id=juego_id)
    user = request.user

    if user in juego.likes.all():
        # Si ya dio like, lo quitamos
        juego.likes.remove(user)
        liked = False
    else:
        # Si no, lo agregamos
        juego.likes.add(user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": juego.likes.count()
    })