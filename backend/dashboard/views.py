from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utilisateurs.decorators import role_required
from dossiers.models import Dossier, Intervention
from audiences.models import Audience
from documents.models import Document
from factures.models import Facture
from utilisateurs.models import User


@login_required
@role_required('admin')
def admin_dashboard(request):
    context = {
        'total_avocats': User.objects.filter(role='avocat').count(),
        'total_assistantes': User.objects.filter(role='assistante').count(),
        'total_dossiers': Dossier.objects.count(),
        'dossiers_ouverts': Dossier.objects.filter(statut='ouvert').count(),
        'total_clients': Dossier.objects.values('client').distinct().count(),
        'audiences': Audience.objects.order_by('date_audience')[:5],
        'equipe': User.objects.filter(role='avocat')[:3],
        'factures_en_attente': Facture.objects.filter(statut='envoyee').count(),
        'total_factures': Facture.objects.count(),
        'recent_dossiers': Dossier.objects.order_by('-date_ouverture')[:5],
        'utilisateurs': User.objects.all().order_by('role'),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@role_required('avocat')
def avocat_dashboard(request):
    mes_dossiers = Dossier.objects.filter(avocat_responsable=request.user)
    context = {
        'mes_dossiers': mes_dossiers.order_by('-date_ouverture')[:5],
        'total_dossiers': mes_dossiers.count(),
        'dossiers_urgents': mes_dossiers.filter(statut='en_cours').count(),
        'mes_audiences': Audience.objects.filter(
            avocat=request.user
        ).order_by('date_audience')[:5],
        'prochaine_audience': Audience.objects.filter(
            avocat=request.user,
            statut='programmee'
        ).order_by('date_audience').first(),
        'mes_interventions': Intervention.objects.filter(
            avocat=request.user
        ).order_by('-date')[:5],
        'mes_documents': Document.objects.filter(
            uploade_par=request.user
        ).count(),
    }
    return render(request, 'dashboard/avocat_dashboard.html', context)


@login_required
@role_required('assistante')
def assistante_dashboard(request):
    user = request.user

    avocat = user.avocat  # OK maintenant (après migration)

    if avocat:
        dossiers = Dossier.objects.filter(avocat_responsable=request.user.avocat)
        audiences = Audience.objects.filter(avocat=avocat)
        documents = Document.objects.filter(dossier__avocat_responsable=avocat)
    else:
        dossiers = Dossier.objects.none()
        audiences = Audience.objects.none()
        documents = Document.objects.none()

    context = {
        'total_dossiers': dossiers.count(),
        'dossiers_recent': dossiers.order_by('-date_ouverture')[:5],
        'audiences_recent': audiences.order_by('-date_audience')[:5],
        'documents_recent': documents.order_by('-date_upload')[:5],
    }

    return render(request, 'dashboard/assistante_dashboard.html', context)
