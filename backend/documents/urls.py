from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_documents, name='liste_documents'),
    path('ajouter/', views.ajouter_document, name='ajouter_document'),
    path('supprimer/<int:id>/', views.supprimer_document, name='supprimer_document'),
]