from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

from apps.blog.models import Juegos
from apps.login.models import PerfilUsuario

from .forms import ComentarioForm
from .models import Comentario

# Create your views here.

def agregar_comentario(request, juego_id):
    juego = get_object_or_404(Juegos, pk=juego_id)

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            try:
                perfil = PerfilUsuario.objects.get(user=request.user)
                Comentario.objects.create(
                    usuario=perfil,
                    blog=juego,
                    texto=texto
                )
                # messages.success(request, "Comentario agregado correctamente ✅")
            except PerfilUsuario.DoesNotExist:
                messages.error(request, "No tienes perfil asociado para comentar.")
        else:
            messages.error(request, "El comentario no puede estar vacío.")

    # Redirigir al perfil y hacer scroll al post comentado
    # return redirect(f"{reverse('perfil')}#post-{juego.id}")

    # Redirigir a la misma página desde la que se envió el comentario
    referer = request.META.get('HTTP_REFERER', reverse('perfil'))
    return redirect(f"{referer}#post-{juego.id}")

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

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comentario.objects.all()
        return Comentario.objects.filter(usuario=self.request.user.perfilusuario)


    def get_success_url(self):
        # Revisar desde qué página vino el usuario
        referer = self.request.META.get('HTTP_REFERER', '')
        if 'perfil' in referer:
            return reverse('perfil') + f"#comentario-{self.object.id}"
        else:
            return reverse('apps.blog:blog') + f"#comentario-{self.object.id}"
    
class EliminarComentario(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentarios/confirmar_eliminacion.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comentario.objects.all()
        return Comentario.objects.filter(usuario=self.request.user.perfilusuario)

    def post(self, request, *args, **kwargs):
        # Obtengo el comentario
        comentario = self.get_object()
        blog_id = comentario.blog.id
        comentario.delete()

        # Detectar si venía del perfil o del blog
        referer = request.META.get('HTTP_REFERER', '')

        if 'perfil' in referer:
            url = reverse('perfil') + f"#post-{blog_id}"
        else:
            url = reverse('apps.blog:blog') + f"#post-{blog_id}"

        return redirect(url)