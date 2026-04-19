from django.urls import path
from . import views

app_name = 'audiences'

urlpatterns = [
    path('', views.liste_audiences, name='liste'),
    path('<int:pk>/', views.detail_audience, name='detail'),
    path('creer/', views.creer_audience, name='creer'),
    path('<int:pk>/modifier/', views.modifier_audience, name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_audience, name='supprimer'),
]