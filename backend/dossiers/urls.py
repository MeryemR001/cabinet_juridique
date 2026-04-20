from django.urls import path
from . import views

app_name = 'dossiers'

urlpatterns = [
    # ── Dossiers ──────────────────────────────────────────────────────────────
    path('liste_dossier', views.liste_dossiers, name='liste'),
    path('<int:pk>/', views.detail_dossier, name='detail'),
    path('creer/', views.creer_dossier, name='creer'),
    path('<int:pk>/modifier/', views.modifier_dossier, name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_dossier, name='supprimer'),

    # ── Clients ───────────────────────────────────────────────────────────────
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/<int:pk>/', views.detail_client, name='detail_client'),
    path('clients/creer/', views.creer_client, name='creer_client'),
    path('clients/ajouter/', views.creer_client, name='client_form'),
    path('clients/<int:pk>/modifier/', views.modifier_client, name='modifier_client'),
    path('clients/<int:pk>/supprimer/', views.supprimer_client, name='supprimer_client'),

    # ── Interventions ─────────────────────────────────────────────────────────
    path('<int:dossier_pk>/intervention/', views.ajouter_intervention, name='ajouter_intervention'),
    path('interventions/', views.liste_interventions, name='liste_interventions'),
    path('interventions/<int:pk>/', views.detail_intervention, name='detail_intervention'),
    path('interventions/<int:pk>/supprimer/', views.supprimer_intervention, name='supprimer_intervention'),
]