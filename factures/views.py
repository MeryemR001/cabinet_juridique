from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django import forms
from utilisateurs.decorators import permission_required
from utilisateurs.permissions import has_role
from utilisateurs.models import User
from .models import Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet
from dossiers.models import Dossier, Client


def _refresh_facture_totals(facture):
    montant_ht = facture.lignes.aggregate(total=Sum('total'))['total'] or 0
    facture.montant_ht = montant_ht
    facture.save()


def _visible_factures_queryset(user):
    if has_role(user, 'admin'):
        return Facture.objects.exclude(statut='annulee')

    if has_role(user, 'avocat'):
        return Facture.objects.filter(avocat=user).exclude(statut='annulee')

    if has_role(user, 'assistante'):
        avocat = getattr(user, 'avocat', None)
        if avocat and has_role(avocat, 'avocat'):
            return Facture.objects.filter(avocat=avocat).exclude(statut='annulee')
        return Facture.objects.none()

    return Facture.objects.none()


def _editable_factures_queryset(user):
    if has_role(user, 'admin'):
        return Facture.objects.all()

    if has_role(user, 'avocat'):
        return Facture.objects.filter(avocat=user)

    return Facture.objects.none()


def _configure_facture_form_for_user(form, user):
    if has_role(user, 'avocat'):
        dossiers_qs = Dossier.objects.filter(avocat_responsable=user)
        clients_qs = Client.objects.filter(
            dossiers__avocat_responsable=user
        ).distinct().order_by('nom', 'prenom')

        form.fields['dossier'].queryset = dossiers_qs
        form.fields['client'].queryset = clients_qs
        form.fields['avocat'].queryset = User.objects.filter(pk=user.pk)
        form.fields['avocat'].initial = user.pk
        form.fields['avocat'].widget = forms.HiddenInput()

        return dossiers_qs.only('id', 'avocat_responsable_id')

    dossiers_qs = Dossier.objects.all()
    form.fields['avocat'].queryset = User.objects.filter(role='avocat')
    return dossiers_qs.only('id', 'avocat_responsable_id')

@login_required
@permission_required('factures.list')
def liste_factures(request):
    factures = _visible_factures_queryset(request.user)

    factures_payees_count = factures.filter(statut='payee').count()
    chiffre_affaires = factures.filter(statut='payee').aggregate(
        total=Sum('montant_ttc')
    )['total'] or 0

    return render(request, 'factures/liste.html', {
        'factures': factures,
        'factures_payees_count': factures_payees_count,
        'chiffre_affaires': chiffre_affaires,
    })

@login_required
@permission_required('factures.detail')
def detail_facture(request, pk):
    facture = get_object_or_404(_visible_factures_queryset(request.user), pk=pk)
    lignes = facture.lignes.all()
    tva_montant = facture.montant_ttc - facture.montant_ht

    return render(request, 'factures/detail.html', {
        'facture': facture,
        'lignes': lignes,
        'tva_montant': tva_montant,
    })

@login_required
@permission_required('factures.create')
def creer_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        dossiers_avocats = _configure_facture_form_for_user(form, request.user)
        formset = LigneFactureFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            facture = form.save(commit=False)
            if has_role(request.user, 'avocat'):
                facture.avocat = request.user
            facture.save()
            formset.instance = facture
            formset.save()
            _refresh_facture_totals(facture)
            return redirect('factures:liste')
    else:
        form = FactureForm()
        dossiers_avocats = _configure_facture_form_for_user(form, request.user)
        formset = LigneFactureFormSet()

    return render(request, 'factures/creer.html', {
        'form': form,
        'formset': formset,
        'dossiers_avocats': dossiers_avocats,
    })

@login_required
@permission_required('factures.update')
def modifier_facture(request, pk):
    facture = get_object_or_404(_editable_factures_queryset(request.user), pk=pk)

    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        dossiers_avocats = _configure_facture_form_for_user(form, request.user)
        formset = LigneFactureFormSet(request.POST, instance=facture)

        if form.is_valid() and formset.is_valid():
            facture = form.save(commit=False)
            if has_role(request.user, 'avocat'):
                facture.avocat = request.user
            facture.save()
            formset.save()
            _refresh_facture_totals(facture)
            return redirect('factures:liste')
        else:
            print(f"Erreurs form: {form.errors}")
            print(f"Erreurs formset: {formset.errors}")
    else:
        form = FactureForm(instance=facture)
        dossiers_avocats = _configure_facture_form_for_user(form, request.user)
        formset = LigneFactureFormSet(instance=facture)

    return render(request, 'factures/creer.html', {
        'form': form,
        'formset': formset,
        'facture': facture,
        'dossiers_avocats': dossiers_avocats,
    })

@login_required
@permission_required('factures.delete')
def supprimer_facture(request, pk):
    facture = get_object_or_404(_editable_factures_queryset(request.user), pk=pk)
    facture.delete()
    return redirect('factures:liste')

@login_required
@permission_required('factures.print')
def imprimer_facture(request, pk):
    facture = get_object_or_404(_visible_factures_queryset(request.user), pk=pk)
    lignes = facture.lignes.all()
    return render(request, 'factures/imprimer.html', {
        'facture': facture,
        'lignes': lignes,
    })