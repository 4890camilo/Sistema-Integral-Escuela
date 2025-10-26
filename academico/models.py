
from django.db import models
from usuarios.models import Usuario

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'ESTUDIANTE'}, related_name='calificaciones_como_estudiante')
    docente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'rol': 'DOCENTE'}, related_name='calificaciones_como_docente')
    curso = models.CharField(max_length=100)
    nota = models.FloatField()
    periodo = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

    def __str__(self):
        return f"{self.estudiante.username} - {self.curso}: {self.nota}"
