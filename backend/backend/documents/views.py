from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from utilisateurs.decorators import role_required
from dossiers.models import Dossier
from .models import Document
from .forms import DocumentForm
import os


@login_required
def liste_documents(request, dossier_pk):
    dossier = get_object_or_404(Dossier, pk=dossier_pk)
    documents = Document.objects.filter(dossier=dossier)
    return render(request, 'documents/liste.html', {
        'dossier': dossier,
        'documents': documents,
    })


@login_required
def upload_document(request, dossier_pk):
    dossier = get_object_or_404(Dossier, pk=dossier_pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploade_par = request.user
            document.dossier = dossier
            document.save()
            return redirect('dossiers:detail', pk=dossier_pk)
    else:
        form = DocumentForm(initial={'dossier': dossier})
    return render(request, 'documents/upload.html', {
        'form': form,
        'dossier': dossier,
    })


@login_required
def telecharger_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    try:
        response = FileResponse(
            open(document.fichier.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(document.fichier.name)
        )
        return response
    except FileNotFoundError:
        raise Http404("Fichier introuvable.")


@login_required
@role_required('admin', 'assistante')
def supprimer_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    dossier_pk = document.dossier.pk
    # Supprime le fichier physique
    if document.fichier and os.path.isfile(document.fichier.path):
        os.remove(document.fichier.path)
    document.delete()
    return redirect('dossiers:detail', pk=dossier_pk)