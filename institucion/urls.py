from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('academico/', include('academico.urls')),
    path('financiero/', include('financiero.urls')),
]