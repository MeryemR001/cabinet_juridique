from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from utilisateurs.decorators import permission_required
from .models import Audience
from .forms import AudienceForm


@login_required
def liste_audiences(request):
    if request.user.role == 'avocat':
        # Avocat voit seulement ses audiences
        audiences = Audience.objects.filter(avocat=request.user).order_by('date_audience')
    else:
        # Admin et assistante voient tout
        audiences = Audience.objects.all().order_by('date_audience')

    audience_status_rows = (
        audiences.values('statut')
        .annotate(total=Count('id'))
        .order_by('statut')
    )
    audience_status_map = {row['statut']: row['total'] for row in audience_status_rows}

    return render(request, 'audiences/liste.html', {
        'audiences': audiences,
        'audience_status_labels': [label for _, label in Audience.STATUTS],
        'audience_status_values': [audience_status_map.get(code, 0) for code, _ in Audience.STATUTS],
    })


@login_required
def detail_audience(request, pk):
    audience = get_object_or_404(Audience, pk=pk)
    return render(request, 'audiences/detail.html', {'audience': audience})


@login_required
@permission_required('audiences.create')
def creer_audience(request):
    if request.method == 'POST':
        form = AudienceForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('audiences:liste')
    else:
        form = AudienceForm(user=request.user)
    return render(request, 'audiences/creer.html', {'form': form})


@login_required
@permission_required('audiences.update')
def modifier_audience(request, pk):
    audience = get_object_or_404(Audience, pk=pk)
    if request.method == 'POST':
        form = AudienceForm(request.POST, instance=audience, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('audiences:detail', pk=pk)
    else:
        form = AudienceForm(instance=audience, user=request.user)
    return render(request, 'audiences/creer.html', {
        'form': form,
        'audience': audience,
    })


@login_required
@permission_required('audiences.delete')
def supprimer_audience(request, pk):
    audience = get_object_or_404(Audience, pk=pk)
    audience.delete()
    return redirect('audiences:liste')