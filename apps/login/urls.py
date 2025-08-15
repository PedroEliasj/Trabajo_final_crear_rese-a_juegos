from django.urls import path
from apps.login import views
from django.contrib.auth import views as auth_views


# app_name = 'apps.login'

urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('usuarios_list/', views.usuarios_list, name='usuarios_list'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    # Recorevy
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='login/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete'),

]

#/login/signup/
#/login/signin/
#/login/logout/
#/login/perfil/
#/login/usuarios_list/
