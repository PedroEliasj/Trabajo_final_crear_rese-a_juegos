from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
from apps.blog.models import Juegos
from apps.login.models import PerfilUsuario

from .forms import ComentarioForm
from apps.comentarios.models import Comentario

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

    def _safe_next(self, next_url: str | None) -> str | None:
        from django.utils.http import url_has_allowed_host_and_scheme
        if not next_url:
            return None
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}, require_https=self.request.is_secure()):
            return next_url
        return None

    def get_success_url(self):
        # next puede venir en GET (form abierto) o POST (tras guardar)
        raw_next = self.request.POST.get('next') or self.request.GET.get('next')
        next_url = self._safe_next(raw_next)
        if next_url:
            return next_url
        # Fallback: volver al blog en el post del comentario
        return reverse('apps.blog:blog') + f"#post-{self.object.blog.id}"
class EliminarComentario(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentarios/confirmar_eliminacion.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comentario.objects.all()
        return Comentario.objects.filter(usuario=self.request.user.perfilusuario)

    def _safe_next(self, next_url: str | None) -> str | None:
        if not next_url:
            return None
        # Permite relativos o del mismo host
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}, require_https=self.request.is_secure()):
            return next_url
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tomamos next de GET (carga de confirmación) o POST (por si vuelve al template por error)
        raw_next = self.request.GET.get('next') or self.request.POST.get('next')
        context['next_url'] = self._safe_next(raw_next) or reverse('apps.blog:blog')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        # Recuperar next del POST (el hidden del template)
        raw_next = request.POST.get('next') or request.GET.get('next')
        next_url = self._safe_next(raw_next)
        # Fallback por si no viene nada
        if not next_url:
            next_url = reverse('apps.blog:blog')

        return redirect(next_url)