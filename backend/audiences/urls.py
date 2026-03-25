from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_audiences, name='liste_audiences'),
    path('ajouter/', views.ajouter_audience, name='ajouter_audience'),
]