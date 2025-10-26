from django.test import TestCase
from django.contrib.auth import get_user_model

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', rol='ESTUDIANTE'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.rol, 'ESTUDIANTE')
        self.assertTrue(self.user.check_password('testpass'))
