from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from utilisateurs.decorators import role_required
from .models import Client, Dossier, Intervention
from .forms import ClientForm, DossierForm, InterventionForm


# ─────────────────────────────────────────
# DOSSIERS
# ─────────────────────────────────────────

@login_required
def liste_dossiers(request):
    if request.user.role == 'avocat':
        dossiers = Dossier.objects.filter(avocat_responsable=request.user)
    else:
        dossiers = Dossier.objects.all()
    return render(request, 'dossiers/liste.html', {'dossiers': dossiers})


@login_required
def detail_dossier(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    interventions = dossier.interventions.all()
    documents = dossier.documents.all()
    audiences = dossier.audiences.all()
    return render(request, 'dossiers/detail.html', {
        'dossier': dossier,
        'interventions': interventions,
        'documents': documents,
        'audiences': audiences,
    })


@login_required
@role_required('admin', 'assistante')
def creer_dossier(request):
    if request.method == 'POST':
        form = DossierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dossiers:liste')
    else:
        form = DossierForm()
    return render(request, 'dossiers/creer.html', {'form': form})


@login_required
@role_required('admin', 'assistante')
def modifier_dossier(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        form = DossierForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            return redirect('dossiers:detail', pk=pk)
    else:
        form = DossierForm(instance=dossier)
    return render(request, 'dossiers/creer.html', {'form': form})


@login_required
@role_required('admin')
def supprimer_dossier(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    dossier.delete()
    return redirect('dossiers:liste')


# ─────────────────────────────────────────
# CLIENTS
# ─────────────────────────────────────────

@login_required
@role_required('admin', 'assistante')
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'dossiers/liste_clients.html', {'clients': clients})


@login_required
@role_required('admin', 'assistante')
def detail_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    dossiers = client.dossiers.select_related('avocat_responsable').order_by('-date_ouverture')

    context = {
        'client': client,
        'dossiers': dossiers,
        'nb_dossiers': dossiers.count(),
        'nb_ouverts': dossiers.filter(statut='ouvert').count(),
        'nb_en_cours': dossiers.filter(statut='en_cours').count(),
        'nb_clos': dossiers.filter(statut='clos').count(),
    }
    return render(request, 'dossiers/detail_client.html', context)


@login_required
@role_required('admin', 'assistante')
def creer_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dossiers:liste_clients')
    else:
        form = ClientForm()
    return render(request, 'dossiers/client_form.html', {'form': form})


@login_required
@role_required('admin', 'assistante')
def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('dossiers:liste_clients')


@login_required
@role_required('admin', 'assistante')
def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('dossiers:liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'dossiers/client_form.html', {'form': form})


# ─────────────────────────────────────────
# INTERVENTIONS
# ─────────────────────────────────────────

@login_required
@role_required('admin', 'assistante', 'avocat')
def ajouter_intervention(request, dossier_pk):
    dossier = get_object_or_404(Dossier, pk=dossier_pk)

    # L'intervention doit toujours etre rattachee a un avocat.
    avocat_pour_intervention = request.user if request.user.role == 'avocat' else dossier.avocat_responsable

    if avocat_pour_intervention is None:
        form = InterventionForm(avocat=request.user, dossier=dossier)
        form.add_error(None, "Ce dossier n'a pas d'avocat responsable. Assignez-en un avant d'ajouter une intervention.")
        return render(request, 'dossiers/intervention_form.html', {
            'form': form,
            'dossier': dossier,
        })

    if request.method == 'POST':
        form = InterventionForm(request.POST, avocat=avocat_pour_intervention, dossier=dossier)
        if form.is_valid():
            form.save()
            return redirect('dossiers:detail', pk=dossier_pk)
    else:
        form = InterventionForm(avocat=avocat_pour_intervention, dossier=dossier)
    return render(request, 'dossiers/intervention_form.html', {
        'form': form,
        'dossier': dossier,
    })


@login_required
def liste_interventions(request):
    """
    Admin & assistante see all interventions.
    Avocat sees only their own.
    """
    if request.user.role == 'avocat':
        interventions = Intervention.objects.filter(avocat=request.user).select_related('dossier', 'avocat').order_by('-date')
    else:
        interventions = Intervention.objects.all().select_related('dossier', 'avocat').order_by('-date')

    total_heures = interventions.aggregate(total=Sum('heures_travaillees'))['total'] or 0
    nb_dossiers_actifs = Dossier.objects.filter(
        interventions__in=interventions
    ).distinct().count()

    return render(request, 'dossiers/liste_interventions.html', {
        'interventions': interventions,
        'total_heures': total_heures,
        'nb_dossiers_actifs': nb_dossiers_actifs,
    })


@login_required
def detail_intervention(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    # Avocat can only see their own
    if request.user.role == 'avocat' and intervention.avocat != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return render(request, 'dossiers/detail_intervention.html', {
        'intervention': intervention,
    })


@login_required
@role_required('admin')
def supprimer_intervention(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    dossier_pk = intervention.dossier.pk
    intervention.delete()
    return redirect('dossiers:detail', pk=dossier_pk)