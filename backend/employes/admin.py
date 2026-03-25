from django.contrib import admin
from .models import Employe

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'email')  # adapte selon tes champs
    search_fields = ('nom', 'prenom', 'email')