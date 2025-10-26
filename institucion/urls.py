# institucion/institucion/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Conecta con la app 'usuarios' (para login, dashboard, etc.)
    path('', include('usuarios.urls')), 
    
    # Conecta con tus otras apps
    path('academico/', include('academico.urls')),
    path('financiero/', include('financiero.urls')),
]