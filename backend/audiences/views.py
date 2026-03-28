from django.shortcuts import render, redirect, get_object_or_404
from .models import Audience
from .forms import AudienceForm

# Liste des audiences
def liste_audiences(request):
    audiences = Audience.objects.all()
    return render(request, 'audiences/liste.html', {'audiences': audiences})

# Ajouter une audience
def ajouter_audience(request):
    if request.method == "POST":
        form = AudienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_audiences')
    else:
        form = AudienceForm()
    return render(request, 'audiences/ajouter.html', {'form': form})

# Modifier une audience
def modifier_audience(request, pk):
    audience = get_object_or_404(Audience, pk=pk)
    if request.method == "POST":
        form = AudienceForm(request.POST, instance=audience)
        if form.is_valid():
            form.save()
            return redirect('liste_audiences')
    else:
        form = AudienceForm(instance=audience)
    return render(request, 'audiences/modifier.html', {'form': form, 'audience': audience})

# Supprimer une audience
def supprimer_audience(request, pk):
    audience = get_object_or_404(Audience, pk=pk)
    audience.delete()
    return redirect('liste_audiences')