# institucion/academico/admin.py
from django.contrib import admin
from .models import Grado, Curso, Materia, Asignacion, Calificacion, Asistencia

# --- Configuración para ver la estructura ---

@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'grado') # Muestra el grado al que pertenece
    list_filter = ('grado',) # Permite filtrar por grado
    search_fields = ('nombre',)

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'grado') # Muestra el grado al que pertenece
    list_filter = ('grado',) # Permite filtrar por grado
    search_fields = ('nombre',)

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('docente', 'materia', 'curso')
    list_filter = ('curso__grado', 'docente') # Filtra por grado o docente
    search_fields = ('docente__username', 'materia__nombre', 'curso__nombre')

# Registramos los otros modelos de forma simple
admin.site.register(Calificacion)
admin.site.register(Asistencia)