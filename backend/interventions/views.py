from django.shortcuts import render, redirect
from .models import Intervention
from dossiers.models import Dossier

def ajouter_intervention(request):
    dossiers = Dossier.objects.all()

    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        date = request.POST.get('date')
        dossier_id = request.POST.get('dossier')

        dossier = Dossier.objects.get(id=dossier_id)

        Intervention.objects.create(
            titre=titre,
            description=description,
            date=date,
            dossier=dossier
        )

        return redirect('liste_interventions')

    return render(request, 'interventions/intervention_list.html', {'dossiers': dossiers})