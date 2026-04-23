from urllib.parse import urlencode

from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from audiences.models import Audience
from dossiers.models import Dossier
from documents.models import Document
from factures.models import Facture
from utilisateurs.models import User
from utilisateurs.permissions import get_dashboard_url_name


def _auth_link(request, target_name, *, kwargs=None):
    target_url = reverse(target_name, kwargs=kwargs or {})
    if request.user.is_authenticated:
        return target_url
    return f"{reverse('utilisateurs:login')}?{urlencode({'next': target_url})}"


def _dashboard_link(request):
    if request.user.is_authenticated:
        return reverse(get_dashboard_url_name(request.user))
    return reverse('utilisateurs:login')


class HomeView(View):
    def get(self, request):
        total_avocats = User.objects.filter(role='avocat').count()
        total_dossiers = Dossier.objects.count()
        dossiers_resolus = Dossier.objects.filter(statut='clos').count()
        dossiers_ouverts = Dossier.objects.filter(statut='ouvert').count()
        dossiers_en_cours = Dossier.objects.filter(statut='en_cours').count()
        dossiers_actifs = dossiers_ouverts + dossiers_en_cours
        total_clients = Dossier.objects.values('client').distinct().count()
        total_audiences = Audience.objects.count()
        documents_total = Document.objects.count()
        factures_en_attente = Facture.objects.filter(statut='envoyee').count()
        chiffre_affaires = Facture.objects.filter(statut='payee').aggregate(
            total=Sum('montant_ttc')
        )['total'] or 0
        taux_succes = round((dossiers_resolus / total_dossiers) * 100) if total_dossiers else 0

        latest_dossier = Dossier.objects.order_by('-date_ouverture').first()
        documents_url = _auth_link(
            request,
            'documents:liste',
            kwargs={'dossier_pk': latest_dossier.pk},
        ) if latest_dossier else _auth_link(request, 'dossiers:liste')

        context = {
            'total_avocats': total_avocats,
            'total_dossiers': total_dossiers,
            'dossiers_resolus': dossiers_resolus,
            'dossiers_ouverts': dossiers_ouverts,
            'dossiers_actifs': dossiers_actifs,
            'total_clients': total_clients,
            'total_audiences': total_audiences,
            'documents_total': documents_total,
            'factures_en_attente': factures_en_attente,
            'chiffre_affaires': chiffre_affaires,
            'taux_succes': taux_succes,
            'cabinet_access_url': _dashboard_link(request),
            'dossiers_url': _auth_link(request, 'dossiers:liste'),
            'audiences_url': _auth_link(request, 'audiences:liste'),
            'clients_url': _auth_link(request, 'dossiers:liste_clients'),
            'documents_url': documents_url,
            'factures_url': _auth_link(request, 'factures:liste'),
        }

        return render(request, 'home/page_accueil.html', context)