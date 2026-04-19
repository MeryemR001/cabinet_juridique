from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from utilisateurs.decorators import role_required
from .models import Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet


@login_required
@role_required('admin', 'avocat')
def liste_factures(request):
    if request.user.role == 'avocat':
        factures = Facture.objects.filter(avocat=request.user)
    else:
        factures = Facture.objects.all()
    return render(request, 'factures/liste.html', {'factures': factures})


@login_required
@role_required('admin', 'avocat')
def detail_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    lignes = facture.lignes.all()
    return render(request, 'factures/detail.html', {
        'facture': facture,
        'lignes': lignes,
    })


@login_required
@role_required('admin', 'avocat')
def creer_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        formset = LigneFactureFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            facture = form.save()
            formset.instance = facture
            formset.save()
            return redirect('factures:detail', pk=facture.pk)
    else:
        form = FactureForm()
        formset = LigneFactureFormSet()
    return render(request, 'factures/creer.html', {
        'form': form,
        'formset': formset,
    })


@login_required
@role_required('admin', 'avocat')
def modifier_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        formset = LigneFactureFormSet(request.POST, instance=facture)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('factures:detail', pk=pk)
    else:
        form = FactureForm(instance=facture)
        formset = LigneFactureFormSet(instance=facture)
    return render(request, 'factures/creer.html', {
        'form': form,
        'formset': formset,
    })


@login_required
@role_required('admin')
def supprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    facture.delete()
    return redirect('factures:liste')


@login_required
@role_required('admin', 'avocat')
def imprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    lignes = facture.lignes.all()
    return render(request, 'factures/imprimer.html', {
        'facture': facture,
        'lignes': lignes,
    })