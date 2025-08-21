from django.shortcuts import get_object_or_404, render

from apps.login.models import PerfilUsuario

def nosotros(request):
    perfil = None
    if request.user.is_authenticated:
        perfil = get_object_or_404(PerfilUsuario, user=request.user)

    return render(request, 'nosotros/nosotros.html', {
        'perfil': perfil
    })