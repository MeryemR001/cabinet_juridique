from django.shortcuts import render, redirect
from .models import Document
from django.shortcuts import get_object_or_404, redirect
from dossiers.models import Dossier

# 📄 Liste documents
def liste_documents(request):
    documents = Document.objects.all()
    return render(request, 'documents/liste.html', {'documents': documents})


# ➕ Ajouter document
def ajouter_document(request):
    dossiers = Dossier.objects.all()

    if request.method == 'POST':
        dossier_id = request.POST.get('dossier')
        fichier = request.FILES.get('fichier')

        dossier = Dossier.objects.get(id=dossier_id)

        Document.objects.create(
            dossier=dossier,
            fichier=fichier
        )
        return redirect('liste_documents')

    return render(request, 'documents/ajouter.html', {'dossiers': dossiers})
def supprimer_document(request, id):
    document = get_object_or_404(Document, id=id)
    document.delete()  # supprime le fichier de la base
    return redirect('liste_documents')