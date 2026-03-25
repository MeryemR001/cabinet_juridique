from django.shortcuts import render
from .models import Facture

def liste_factures(request):
    factures = Facture.objects.all()
    return render(request, 'factures/facture_list.html', {'factures': factures})