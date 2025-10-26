# institucion/usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- Rutas de Autenticación y Panel ---
    
    # Dejamos tu ruta de login original
    path('login/', views.login_view, name='login'), 
    
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    
    # --- Rutas del CRUD de Personal ---
    
    # /personal/registrar/
    path('personal/registrar/', views.registrar_personal_view, name='registrar_personal'),
    
    # /personal/consultar/
    path('personal/consultar/', views.consultar_personal_view, name='consultar_personal'),
    
    # /personal/editar/1/
    path('personal/editar/<int:pk>/', views.editar_personal_view, name='editar_personal'),
    
    # /personal/eliminar/1/
    path('personal/eliminar/<int:pk>/', views.eliminar_personal_view, name='eliminar_personal'),
]