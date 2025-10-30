# institucion/academico/models.py
from django.db import models
from django.conf import settings # Para traer tu modelo 'Usuario'
from django.core.exceptions import ValidationError

# --- 1. MODELOS DE ESTRUCTURA ---
# (Estos son tus modelos existentes, están perfectos)

class Grado(models.Model):
    """ El nivel académico. Ej: "Primero", "Segundo", "Once" """
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Curso(models.Model):
    """ El salón específico. Ej: "Primero A", "Primero B" """
    nombre = models.CharField(max_length=100, unique=True)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='cursos')
    
    def __str__(self):
        return self.nombre

class Materia(models.Model):
    """ La materia específica para un grado. Ej: "Matemáticas (Primero)" """
    nombre = models.CharField(max_length=100) # Ej: "Matemáticas"
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='materias')
    
    class Meta:
        unique_together = ('nombre', 'grado')
    
    def __str__(self):
        return f"{self.nombre} ({self.grado.nombre})"

class Asignacion(models.Model):
    """ Conecta: Docente, Materia (de un grado) y Curso (de ese grado). """
    docente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asignaciones_docente')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='asignaciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asignaciones')
    
    class Meta:
        unique_together = ('docente', 'materia', 'curso')
    
    def __str__(self):
        return f"{self.materia} -> {self.curso.nombre} ({self.docente.username})"
    
    def clean(self):
        if self.materia.grado != self.curso.grado:
            raise ValidationError(
                f"Error: La materia '{self.materia}' es del grado {self.materia.grado.nombre} "
                f"pero el curso '{self.curso}' es del grado {self.curso.grado.nombre}."
            )

# --- 2. MODELOS DE ACCIÓN (CALIFICACIONES Y ASISTENCIA) ---
# (Estos también son tus modelos existentes)

class Calificacion(models.Model):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calificaciones')
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    periodo = models.CharField(max_length=50) # Concepto (Trimestre 1, Taller 1)
    fecha = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.asignacion.materia.nombre}: {self.nota}"

class Asistencia(models.Model):
    ESTADOS = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('TARDANZA', 'Tardanza'),
        ('JUSTIFICADO', 'Justificado'),
    ]
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asistencias')
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PRESENTE')
    
    class Meta:
        unique_together = ('estudiante', 'asignacion', 'fecha')
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.fecha}: {self.estado}"

# --- 3. ¡NUEVO MODELO PARA MATERIAL DIDÁCTICO! (RF-007 y RF-008) ---

class MaterialDidactico(models.Model):
    """
    Un archivo (RF-008) o texto (RF-007) subido por un docente
    para una asignación específica.
    """
    # 1. A qué asignación pertenece (Docente, Materia, Curso)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name='materiales')
    
    # 2. Datos del material
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True) # Para RF-007 (crear material)
    
    # 3. El archivo (RF-008)
    # Los archivos se guardarán en /media/materiales_docentes/
    archivo = models.FileField(upload_to='materiales_docentes/', blank=True, null=True) 
    
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.asignacion.materia.nombre}"
    
    def clean(self):
        # Validación: Debe tener una descripción o un archivo, no puede estar vacío.
        if not self.descripcion and not self.archivo:
            raise ValidationError("El material debe tener al menos una descripción o un archivo adjunto.")