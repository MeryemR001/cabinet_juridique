from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('dossier/<int:dossier_pk>/', views.liste_documents, name='liste'),
    path('dossier/<int:dossier_pk>/upload/', views.upload_document, name='upload'),
    path('<int:pk>/telecharger/', views.telecharger_document, name='telecharger'),
    path('<int:pk>/supprimer/', views.supprimer_document, name='supprimer'),
]