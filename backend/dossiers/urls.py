# dossiers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dossier_list, name='dossier_list'),
]