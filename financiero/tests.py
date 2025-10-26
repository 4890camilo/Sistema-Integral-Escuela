from django.test import TestCase
from usuarios.models import Usuario
from .models import Pago

class PagoTestCase(TestCase):
    def setUp(self):
        self.estudiante = Usuario.objects.create_user(username='estudiante', password='pass', rol='ESTUDIANTE')
        self.admin = Usuario.objects.create_user(username='admin', password='pass', rol='ADMINISTRATIVO')
        self.pago = Pago.objects.create(
            estudiante=self.estudiante, administrativo=self.admin, monto=500.00, fecha_pago='2025-10-20', estado='PAGADO'
        )

    def test_pago_creation(self):
        self.assertEqual(str(self.pago), 'estudiante - 500.00 (PAGADO)')