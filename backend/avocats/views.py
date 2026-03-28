from django.shortcuts import render, redirect, get_object_or_404
from .models import Avocat, Assistante
from .forms import AvocatForm, AssistanteForm

# ================== AVOCATS ==================
def liste_avocats(request):
    avocats = Avocat.objects.all()
    return render(request, 'avocats/liste.html', {'avocats': avocats})

def ajouter_avocat(request):
    if request.method == 'POST':
        form = AvocatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_avocats')
    else:
        form = AvocatForm()
    return render(request, 'avocats/ajouter.html', {'form': form})

def modifier_avocat(request, avocat_id):
    avocat = get_object_or_404(Avocat, id=avocat_id)
    if request.method == 'POST':
        form = AvocatForm(request.POST, instance=avocat)
        if form.is_valid():
            form.save()
            return redirect('liste_avocats')
    else:
        form = AvocatForm(instance=avocat)
    return render(request, 'avocats/modifier.html', {'form': form, 'avocat': avocat})

def supprimer_avocat(request, avocat_id):
    avocat = get_object_or_404(Avocat, id=avocat_id)
    avocat.delete()
    return redirect('liste_avocats')


# ================== ASSISTANTES ==================
def liste_assistantes(request):
    assistantes = Assistante.objects.select_related('avocat').all()
    return render(request, 'avocats/liste_assistantes.html', {'assistantes': assistantes})

def ajouter_assistante(request):
    if request.method == 'POST':
        form = AssistanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_assistantes')
    else:
        form = AssistanteForm()
    return render(request, 'avocats/ajouter_assistante.html', {'form': form})

def modifier_assistante(request, assistante_id):
    assistante = get_object_or_404(Assistante, id=assistante_id)
    if request.method == 'POST':
        form = AssistanteForm(request.POST, instance=assistante)
        if form.is_valid():
            form.save()
            return redirect('liste_assistantes')
    else:
        form = AssistanteForm(instance=assistante)
    return render(request, 'avocats/modifier_assistante.html', {'form': form, 'assistante': assistante})

def supprimer_assistante(request, assistante_id):
    assistante = get_object_or_404(Assistante, id=assistante_id)
    assistante.delete()
    return redirect('liste_assistantes')