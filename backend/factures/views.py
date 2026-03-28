from django.shortcuts import render

def liste_factures(request):
    return render(request, 'factures/liste_factures.html')