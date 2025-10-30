# institucion/academico/management/commands/poblar_datos_prueba.py
from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from academico.models import Grado, Curso, Materia, Asignacion

class Command(BaseCommand):
    help = 'Puebla la BD con datos de prueba (asignaciones y estudiantes)'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando la carga de datos de prueba...")

        # --- 1. Buscamos los usuarios de prueba ---
        try:
            docente_prueba = Usuario.objects.get(username='docente_prueba')
            estudiante_prueba = Usuario.objects.get(username='estudiante_prueba')
        except Usuario.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                "Error: No se encontraron 'docente_prueba' o 'estudiante_prueba'."
                "Por favor, créalos primero desde 'Gestión de Personal'."
            ))
            return

        # --- 2. Buscamos la estructura (Grados, Cursos, Materias) ---
        try:
            grado_decimo = Grado.objects.get(nombre='Décimo')
            curso_decimo_a = Curso.objects.get(nombre='Décimo A')
            
            # Buscamos materias que pertenecen al grado Décimo
            materia_matematicas = Materia.objects.get(nombre='Matemáticas', grado=grado_decimo)
            materia_fisica = Materia.objects.get(nombre='Física', grado=grado_decimo)
            
        except (Grado.DoesNotExist, Curso.DoesNotExist, Materia.DoesNotExist) as e:
            self.stderr.write(self.style.ERROR(
                f"Error: No se encontró la estructura académica. ¿Corriste las migraciones? ({e})"
            ))
            return

        # --- 3. Asignamos el estudiante a un curso ---
        estudiante_prueba.curso = curso_decimo_a
        estudiante_prueba.save()
        
        self.stdout.write(self.style.SUCCESS(
            f"Se asignó al estudiante '{estudiante_prueba.username}' al curso '{curso_decimo_a.nombre}'."
        ))

        # --- 4. Creamos las Asignaciones para el docente ---
        asignacion1, c1 = Asignacion.objects.get_or_create(
            docente=docente_prueba,
            materia=materia_matematicas,
            curso=curso_decimo_a
        )
        
        asignacion2, c2 = Asignacion.objects.get_or_create(
            docente=docente_prueba,
            materia=materia_fisica,
            curso=curso_decimo_a
        )

        if c1 or c2:
            self.stdout.write(self.style.SUCCESS(
                f"Se asignó a '{docente_prueba.username}' para dar Matemáticas y Física en Décimo A."
            ))
        else:
            self.stdout.write(self.style.WARNING(
                "Las asignaciones para 'docente_prueba' ya existían."
            ))

        self.stdout.write(self.style.SUCCESS("¡Script de población de datos completado! 🚀"))