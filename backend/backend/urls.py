from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('utilisateurs/', include('utilisateurs.urls', namespace='utilisateurs')),  # ✅ une seule inclusion
    path('dashboard/', include('dashboard.urls')),
    path('dossiers/', include('dossiers.urls')),
    path('documents/', include('documents.urls')),
    path('audiences/', include('audiences.urls')),
    path('factures/', include('factures.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)