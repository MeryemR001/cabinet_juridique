from django.urls import path
from . import views

app_name = 'factures'

urlpatterns = [
    path('', views.liste_factures, name='liste'),
    path('<int:pk>/', views.detail_facture, name='detail'),
    path('creer/', views.creer_facture, name='creer'),
    path('<int:pk>/modifier/', views.modifier_facture, name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_facture, name='supprimer'),
    path('<int:pk>/imprimer/', views.imprimer_facture, name='imprimer'),
]