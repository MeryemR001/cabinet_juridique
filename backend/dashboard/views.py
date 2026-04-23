from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils import timezone

from utilisateurs.decorators import role_required
from dossiers.models import Dossier, Intervention
from audiences.models import Audience
from documents.models import Document
from factures.models import Facture
from utilisateurs.models import User


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


@login_required
@role_required('admin')
def admin_dashboard(request):
    aujourd_hui = timezone.now().date()
    current_year = aujourd_hui.year

    annual_revenue_rows = (
        Facture.objects.filter(statut='payee', date_emission__year=current_year)
        .annotate(month=ExtractMonth('date_emission'))
        .values('month')
        .annotate(total=Sum('montant_ttc'))
        .order_by('month')
    )

    revenue_by_avocat_rows = (
        Facture.objects.filter(statut='payee', avocat__isnull=False)
        .values('avocat__first_name', 'avocat__last_name')
        .annotate(total=Sum('montant_ttc'))
        .order_by('-total', 'avocat__last_name', 'avocat__first_name')
    )

    revenue_by_avocat_total = sum(float(row['total'] or 0) for row in revenue_by_avocat_rows)

    clients_by_avocat_rows = (
        Dossier.objects.filter(avocat_responsable__isnull=False)
        .values('avocat_responsable__first_name', 'avocat_responsable__last_name')
        .annotate(total_clients=Count('client', distinct=True))
        .order_by('-total_clients', 'avocat_responsable__last_name', 'avocat_responsable__first_name')
    )

    audience_status_rows = (
        Audience.objects.values('statut')
        .annotate(total=Count('id'))
        .order_by('statut')
    )
    audience_status_map = {row['statut']: row['total'] for row in audience_status_rows}

    revenue_labels = [f"{row['avocat__first_name']} {row['avocat__last_name']}".strip() for row in revenue_by_avocat_rows]
    revenue_values = [float(row['total'] or 0) for row in revenue_by_avocat_rows]
    revenue_percentages = [
        round((float(row['total'] or 0) / revenue_by_avocat_total) * 100, 1)
        if revenue_by_avocat_total else 0
        for row in revenue_by_avocat_rows
    ]
    client_labels = [f"{row['avocat_responsable__first_name']} {row['avocat_responsable__last_name']}".strip() for row in clients_by_avocat_rows]
    client_values = [row['total_clients'] for row in clients_by_avocat_rows]
    audience_labels = [label for _, label in Audience.STATUTS]
    audience_values = [audience_status_map.get(code, 0) for code, _ in Audience.STATUTS]

    # Monthly revenue labels and values
    month_names = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    annual_revenue_labels = [month_names[row['month'] - 1] for row in annual_revenue_rows if row['month'] is not None]
    annual_revenue_values = [float(row['total'] or 0) for row in annual_revenue_rows if row['month'] is not None]

    context = {
        'total_avocats': User.objects.filter(role='avocat').count(),
        'total_assistantes': User.objects.filter(role='assistante').count(),
        'total_dossiers': Dossier.objects.count(),
        'dossiers_ouverts': Dossier.objects.filter(statut='ouvert').count(),
        'total_clients': Dossier.objects.values('client').distinct().count(),
        'audiences': Audience.objects.order_by('date_audience')[:5],
        'audiences_mois': Audience.objects.filter(date_audience__gte=timezone.now()).exclude(statut='annulee').order_by('date_audience'),
        'equipe': User.objects.filter(role='avocat')[:3],
        'factures_en_attente': Facture.objects.filter(statut='envoyee').count(),
        'total_factures': Facture.objects.count(),
        'chiffre_affaires': Facture.objects.filter(statut='payee').aggregate(total=Sum('montant_ttc'))['total'] or 0,
        'recent_dossiers': Dossier.objects.order_by('-date_ouverture')[:5],
        'utilisateurs': User.objects.all().order_by('role'),
        'annual_revenue_labels': annual_revenue_labels,
        'annual_revenue_values': annual_revenue_values,
        'avocat_revenue_labels': revenue_labels,
        'avocat_revenue_values': revenue_values,
        'avocat_revenue_percentages': revenue_percentages,
        'avocat_client_labels': client_labels,
        'avocat_client_values': client_values,
        'audience_status_labels': audience_labels,
        'audience_status_values': audience_values,
        'revenue_avocat_labels': revenue_labels,
        'revenue_avocat_values': revenue_values,
        'revenue_avocat_percentages': revenue_percentages,
        'clients_avocat_labels': client_labels,
        'clients_avocat_values': client_values,
        'aujourd_hui': aujourd_hui,
        'dashboard_greeting': _dashboard_greeting(request.user),
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@role_required('avocat')
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
        'prochaine_audience': Audience.objects.filter(avocat=request.user, statut='programmee').order_by('date_audience').first(),
        'mes_interventions': Intervention.objects.filter(avocat=request.user).order_by('-date')[:5],
        'mes_documents': Document.objects.filter(uploade_par=request.user).count(),
        'dashboard_greeting': _dashboard_greeting(request.user),
    }

    return render(request, 'dashboard/avocat_dashboard.html', context)


@login_required
@role_required('assistante')
def assistante_dashboard(request):
    user = request.user

    avocat = getattr(user, 'avocat', None)
    if avocat and avocat.role != 'avocat':
        avocat = None

    if avocat:
        dossiers = Dossier.objects.filter(avocat_responsable=avocat)
        audiences = Audience.objects.filter(avocat=avocat)
    else:
        dossiers = Dossier.objects.none()
        audiences = Audience.objects.none()

    audience_metrics = _audience_metrics(audiences)
    audiences_total = audience_metrics['audiences_success_count'] + audience_metrics['audiences_failed_count']
    if audiences_total:
        audiences_success_pct = round((audience_metrics['audiences_success_count'] / audiences_total) * 100)
        audiences_failed_pct = round((audience_metrics['audiences_failed_count'] / audiences_total) * 100)
    else:
        audiences_success_pct = 0
        audiences_failed_pct = 0

    chiffre_affaires = Facture.objects.filter(avocat=avocat, statut='payee').aggregate(total=Sum('montant_ttc'))['total'] or 0 if avocat else 0

    context = {
        'total_dossiers': dossiers.count(),
        'dossiers_recent': dossiers.order_by('-date_ouverture')[:5],
        'audiences_recent': audiences.order_by('-date_audience')[:5],
        'audiences_a_planifier': audiences.filter(date_audience__gte=timezone.now(), statut='programmee').count(),
        'chiffre_affaires': chiffre_affaires,
        'audiences_success_pct': audiences_success_pct,
        'audiences_failed_pct': audiences_failed_pct,
        **audience_metrics,
        'dashboard_greeting': _dashboard_greeting(user),
    }

    return render(request, 'dashboard/assistante_dashboard.html', context)
