from django.shortcuts import render
from .models import Dossier

def dossier_list(request):
    dossiers = Dossier.objects.all()
    return render(request, 'dossiers/dossier_list.html', {'dossiers': dossiers})