from django.urls import path
from .views import liste_factures

urlpatterns = [
    path('', liste_factures, name='facture_list'),
]