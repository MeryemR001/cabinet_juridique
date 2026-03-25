from django.urls import path
from .views import ajouter_intervention

urlpatterns = [
    path('ajouter/', ajouter_intervention, name='ajouter_intervention'),
]