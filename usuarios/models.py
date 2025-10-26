from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class Usuario(AbstractUser):
    ROLES = (
        ('ADMINISTRATIVO', 'Administrativo'),
        ('DOCENTE', 'Docente'),
        ('ESTUDIANTE', 'Estudiante'),
        ('PADRES', 'Padres'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    telefono = models.CharField(max_length=15, blank=True, null=True, help_text="Número de teléfono (requerido para Padres)")
    correo = models.EmailField(max_length=254, blank=True, null=True, validators=[EmailValidator()], help_text="Correo electrónico (requerido para Padres)")
    direccion = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_rol_display(self):
        return dict(self.ROLES).get(self.rol, 'Desconocido')

    def clean(self):
        if self.rol == 'PADRES':
            if not self.telefono:
                raise ValidationError({'telefono': 'El teléfono es requerido para Padres.'})
            if not self.correo:
                raise ValidationError({'correo': 'El correo es requerido para Padres.'})