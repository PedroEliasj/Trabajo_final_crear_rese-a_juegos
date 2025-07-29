from django.urls import path
from apps.login import views

urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('perfil/', views.ver_perfil, name='perfil'),
    path('usuarios_list/', views.usuarios_list, name='usuarios_list'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]

#/login/signup/
#/login/signin/
#/login/logout/
#/login/perfil/
#/login/usuarios_list/
