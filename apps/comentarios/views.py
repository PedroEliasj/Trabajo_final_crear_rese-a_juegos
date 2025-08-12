from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

from apps.login.models import PerfilUsuario

from .forms import ComentarioForm
from .models import Comentario

# Create your views here.

def agregar_comentario(request):
    form = ComentarioForm(request.POST or None)

    if form.is_valid():
        comentario = form.save(commit=False)
        if request.user.is_authenticated:
            try:
                perfil = PerfilUsuario.objects.get(user=request.user)
                comentario.usuario = perfil
                comentario.save()
                form = ComentarioForm()
            except PerfilUsuario.DoesNotExist:
                pass

    template_name = 'comentarios/agregar_comentario.html'
    context = {
        'form' : form
    }
    return render(request, template_name, context)

def listar_comentarios(request):
    comentarios = Comentario.objects.all()
    template_name = 'comentarios/listar_comentario.html'

    context = {
        'comentarios' : comentarios
    }
    return render(request, template_name, context)

class ModificarComentario(LoginRequiredMixin, UpdateView):
    model = Comentario
    fields = ['texto']
    template_name = 'comentarios/agregar_comentario.html'
    success_url = reverse_lazy('apps.blog:lista_juegos')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(usuario = self.request.user.perfilusuario)

        return queryset
    
class EliminarComentario(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentarios/confirmar_eliminacion.html'  
    success_url = reverse_lazy('apps.blog:lista_juegos')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user.perfilusuario)