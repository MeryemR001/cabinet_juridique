from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from utilisateurs.decorators import role_required
from .models import Client, Dossier, Intervention
from .forms import ClientForm, DossierForm, InterventionForm


# ─────────────────────────────────────────
# DOSSIERS
# ─────────────────────────────────────────

@login_required
def liste_dossiers(request):
    # Avocat voit seulement ses dossiers
    if request.user.role == 'avocat':
        dossiers = Dossier.objects.filter(avocat_responsable=request.user)
    else:
        # Admin et assistante voient tout
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
def creer_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dossiers:liste_clients')
    else:
        form = ClientForm()
    return render(request, 'dossiers/client_form.html', {'form': form})
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
@role_required('avocat')
def ajouter_intervention(request, dossier_pk):
    dossier = get_object_or_404(Dossier, pk=dossier_pk)
    if request.method == 'POST':
        form = InterventionForm(request.POST, avocat=request.user)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.avocat = request.user
            intervention.dossier = dossier
            intervention.save()
            return redirect('dossiers:detail', pk=dossier_pk)
    else:
        form = InterventionForm(avocat=request.user)
    return render(request, 'dossiers/intervention_form.html', {
        'form': form,
        'dossier': dossier
    })