from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_factures, name='liste_factures'),
]