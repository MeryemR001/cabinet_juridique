from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from utilisateurs.decorators import permission_required
from utilisateurs.models import User

from dossiers.models import Dossier, Intervention
from audiences.models import Audience
from documents.models import Document
from factures.models import Facture


def _dashboard_greeting(user):
    display_name = user.last_name or user.first_name or user.get_full_name() or user.username

    if user.role == 'avocat':
        return f"Bonjour, Maître {display_name}"
    if user.role == 'assistante':
        return f"Bonjour, Assistante {display_name}"
    return f"Bonjour, {display_name}"


def _audience_metrics(audiences_queryset):
    return {
        'audiences_success_count': audiences_queryset.filter(statut='tenue').count(),
        'audiences_failed_count': audiences_queryset.filter(statut='annulee').count(),
        'audiences_mois': audiences_queryset.filter(
            date_audience__gte=timezone.now()
        ).exclude(statut='annulee').order_by('date_audience'),
    }


# =========================
# 🔵 ADMIN DASHBOARD
# =========================
@login_required
@permission_required('dashboard.admin')
def admin_dashboard(request):
    aujourd_hui = timezone.now().date()

    context = {
        'total_avocats': User.objects.filter(role='avocat').count(),
        'total_assistantes': User.objects.filter(role='assistante').count(),

        'total_dossiers': Dossier.objects.count(),
        'dossiers_ouverts': Dossier.objects.filter(statut='ouvert').count(),

        'total_clients': Dossier.objects.values('client').distinct().count(),

        'audiences': Audience.objects.order_by('date_audience')[:5],
        'audiences_mois': Audience.objects.filter(
            date_audience__gte=timezone.now()
        ).exclude(statut='annulee').order_by('date_audience'),

        'equipe': User.objects.filter(role='avocat')[:3],

        'factures_en_attente': Facture.objects.filter(statut='envoyee').count(),
        'total_factures': Facture.objects.exclude(statut='annulee').count(),

        'chiffre_affaires': Facture.objects.filter(statut='payee').aggregate(
            total=Sum('montant_ttc')
        )['total'] or 0,

        'recent_dossiers': Dossier.objects.order_by('-date_ouverture')[:5],
        'utilisateurs': User.objects.all().order_by('role'),

        'aujourd_hui': aujourd_hui,
        'dashboard_greeting': _dashboard_greeting(request.user),
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


# =========================
# ⚖️ AVOCAT DASHBOARD
# =========================
@login_required
@permission_required('dashboard.avocat')
def avocat_dashboard(request):
    mes_dossiers = Dossier.objects.filter(avocat_responsable=request.user)
    mes_audiences = Audience.objects.filter(avocat=request.user)
    audience_metrics = _audience_metrics(mes_audiences)

    context = {
        'mes_dossiers': mes_dossiers.order_by('-date_ouverture')[:5],
        'total_dossiers': mes_dossiers.count(),
        'dossiers_urgents': mes_dossiers.filter(statut='en_cours').count(),

        'mes_audiences': mes_audiences.order_by('date_audience')[:5],
        **audience_metrics,

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
        'dashboard_greeting': _dashboard_greeting(request.user),
    }

    return render(request, 'dashboard/avocat_dashboard.html', context)


# =========================
# 🧾 ASSISTANTE DASHBOARD
# =========================
@login_required
@permission_required('dashboard.assistante')
def assistante_dashboard(request):
    user = request.user

    avocat = getattr(user, 'avocat', None)
    if avocat and avocat.role != 'avocat':
        avocat = None

    if avocat:
        dossiers = Dossier.objects.filter(avocat_responsable=avocat)
        audiences = Audience.objects.filter(avocat=avocat)
        factures = Facture.objects.filter(avocat=avocat).exclude(statut='annulee')
    else:
        dossiers = Dossier.objects.none()
        audiences = Audience.objects.none()
        factures = Facture.objects.none()

    audience_metrics = _audience_metrics(audiences)
    audiences_total = audience_metrics['audiences_success_count'] + audience_metrics['audiences_failed_count']
    if audiences_total:
        audiences_success_pct = round((audience_metrics['audiences_success_count'] / audiences_total) * 100)
        audiences_failed_pct = round((audience_metrics['audiences_failed_count'] / audiences_total) * 100)
    else:
        audiences_success_pct = 0
        audiences_failed_pct = 0

    chiffre_affaires = factures.filter(statut='payee').aggregate(
        total=Sum('montant_ttc')
    )['total'] or 0

    context = {
        'total_dossiers': dossiers.count(),
        'dossiers_recent': dossiers.order_by('-date_ouverture')[:5],
        'audiences_recent': audiences.order_by('-date_audience')[:5],
        'audiences_a_planifier': audiences.filter(
            date_audience__gte=timezone.now(),
            statut='programmee'
        ).count(),
        'chiffre_affaires': chiffre_affaires,
        'audiences_success_pct': audiences_success_pct,
        'audiences_failed_pct': audiences_failed_pct,
        **audience_metrics,
        'dashboard_greeting': _dashboard_greeting(user),
    }

    return render(request, 'dashboard/assistante_dashboard.html', context)