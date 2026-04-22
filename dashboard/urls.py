from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin'),
    path('avocat/', views.avocat_dashboard, name='avocat'),
    path('assistante/', views.assistante_dashboard, name='assistante'),
   
]