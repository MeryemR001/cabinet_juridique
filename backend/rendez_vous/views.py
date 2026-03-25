from django.shortcuts import render
from .models import RendezVous

def liste_rendezvous(request):
    rendezvous = RendezVous.objects.all()
    return render(request, 'rendezvous/rendezvous_list.html', {'rendezvous': rendezvous})