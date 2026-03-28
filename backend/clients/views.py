from django.shortcuts import render, redirect, get_object_or_404
from .models import Client

# 📄 Liste des clients
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste.html', {'clients': clients})


# ➕ Ajouter client
def ajouter_client(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')

        Client.objects.create(
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            email=email
        )
        return redirect('liste_clients')

    return render(request, 'clients/ajouter.html')


# ✏️ Modifier client
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.prenom = request.POST.get('prenom')
        client.telephone = request.POST.get('telephone')
        client.email = request.POST.get('email')
        client.save()

        return redirect('liste_clients')

    return render(request, 'clients/modifier.html', {'client': client})


# ❌ Supprimer client
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('liste_clients')