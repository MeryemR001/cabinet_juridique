from django.shortcuts import render
from dossiers.models import Dossier
from clients.models import Client
from documents.models import Document
from audiences.models import Audience
from .models import Tache
from datetime import date

def dashboard(request):
    # 5 derniers dossiers
    dossiers_recents = Dossier.objects.all().order_by('-date_creation')[:5]

    # Stats
    total_dossiers_actifs = Dossier.objects.filter(statut='en_cours').count()
    total_dossiers_clos   = Dossier.objects.filter(statut='cloture').count()
    total_clients         = Client.objects.count()
    total_documents       = Document.objects.count()
    total_rdv             = Audience.objects.filter(date_audience__gte=date.today()).count()

    # 5 premières tâches
    taches = Tache.objects.all()[:5]

    # Context pour le template
    context = {
        'dossiers_recents': dossiers_recents,
        'total_dossiers_actifs': total_dossiers_actifs,
        'total_dossiers_clos': total_dossiers_clos,
        'total_clients': total_clients,
        'total_documents': total_documents,
        'total_rdv': total_rdv,
        'taches': taches,
    }

    return render(request, 'dashboard/dashboard.html', context)