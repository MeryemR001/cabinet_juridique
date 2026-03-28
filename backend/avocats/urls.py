from django.urls import path
from . import views

urlpatterns = [
    path('avocats/', views.liste_avocats, name='liste_avocats'),
    path('avocats/ajouter/', views.ajouter_avocat, name='ajouter_avocat'),
    path('avocats/modifier/<int:avocat_id>/', views.modifier_avocat, name='modifier_avocat'),
    path('avocats/supprimer/<int:avocat_id>/', views.supprimer_avocat, name='supprimer_avocat'),
]