from django.test import TestCase
from usuarios.models import Usuario
from .models import Calificacion

class CalificacionTestCase(TestCase):
    def setUp(self):
        self.estudiante = Usuario.objects.create_user(username='estudiante', password='pass', rol='ESTUDIANTE')
        self.docente = Usuario.objects.create_user(username='docente', password='pass', rol='DOCENTE')
        self.calificacion = Calificacion.objects.create(
            estudiante=self.estudiante, docente=self.docente, curso='Matemáticas', nota=9.5, periodo='2025-1'
        )

    def test_calificacion_creation(self):
        self.assertEqual(str(self.calificacion), 'estudiante - Matemáticas: 9.5')
