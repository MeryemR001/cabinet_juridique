from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_dossiers, name='liste_dossiers'),
    path('ajouter/', views.ajouter_dossier, name='ajouter_dossier'),
path('modifier/<int:pk>/', views.modifier_dossier, name='modifier_dossier'),
path('supprimer/<int:pk>/', views.supprimer_dossier, name='supprimer_dossier')
]