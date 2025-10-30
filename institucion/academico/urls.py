# institucion/academico/urls.py
from django.urls import path
from . import views

app_name = 'academico' 

urlpatterns = [
    # --- RUTAS HUB DOCENTE ---
    path('calificaciones/seleccionar/', views.hub_calificaciones_view, name='hub_calificaciones'),
    path('asistencia/seleccionar/', views.hub_asistencia_view, name='hub_asistencia'),
    path('material/seleccionar/', views.hub_material_view, name='hub_material'), 

    # --- RUTAS DE ACCIÓN DOCENTE ---
    path('calificaciones/ingresar/<int:pk>/', views.ingresar_calificaciones_view, name='ingresar_calificaciones'),
    path('asistencia/registrar/<int:pk>/', views.registrar_asistencia_view, name='registrar_asistencia'),
    path('material/gestionar/<int:pk>/', views.gestionar_material_view, name='gestionar_material'),
    path('material/eliminar/<int:pk>/', views.eliminar_material_view, name='eliminar_material'),
    
    # --- RUTAS DE ADMIN ---
    path('asignaciones/', views.listar_asignaciones_view, name='listar_asignaciones'),
    path('asignaciones/crear/', views.crear_asignacion_view, name='crear_asignacion'),

    # --- RUTAS DE ESTUDIANTE ---
    path('mis-calificaciones/', views.ver_calificaciones_view, name='ver_calificaciones'), # (RF-003)
    path('mis-asistencias/', views.ver_asistencia_view, name='ver_asistencia'), # (RF-006)
    
    # ¡ESTA ES LA LÍNEA QUE FALTABA! (RF-009)
    path('mis-materiales/', views.ver_material_view, name='ver_material'),
]