from django.shortcuts import render
from .models import Audience

def liste_audiences(request):
    audiences = Audience.objects.all()
    return render(request, 'audiences/audience_list.html', {'audiences': audiences})