from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.liste_utilisateurs, name='liste'),
    path('creer/', views.creer_utilisateur, name='creer'),
    path('<int:pk>/modifier/', views.modifier_utilisateur, name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_utilisateur, name='supprimer'),
]