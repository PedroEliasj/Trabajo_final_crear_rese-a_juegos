from django.urls import path
from apps.login import views

urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
]

#/login/signup/
#/login/signin/
#/login/logout/