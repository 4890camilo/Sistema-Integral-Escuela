# institucion/usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Usuario(AbstractUser):
    # Definimos los roles
    ADMINISTRATIVO = 'ADMINISTRATIVO'
    DOCENTE = 'DOCENTE'
    ESTUDIANTE = 'ESTUDIANTE'
    PADRES = 'PADRES'
    ROLES = [
        (ADMINISTRATIVO, 'Administrativo'),
        (DOCENTE, 'Docente'),
        (ESTUDIANTE, 'Estudiante'),
        (PADRES, 'Padres'),
    ]

    # --- Tus campos personalizados ---
    rol = models.CharField(max_length=20, choices=ROLES, default=ESTUDIANTE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    # --- ¡CAMPO REACTIVADO! ---
    # Ahora que las tablas base existen, volvemos a activar este campo.
    
    curso = models.ForeignKey(
        "academico.Curso",  # Usamos comillas para evitar errores
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estudiantes' 
    )

    # Campos de autenticación de Django (con related_name)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_groups', # Nombre único
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_permissions', # Nombre único
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_rol_display(self):
        return dict(self.ROLES).get(self.rol)

    def clean(self):
        super().clean()
        if self.rol == self.PADRES and (not self.telefono or not self.correo):
            raise ValidationError('Los padres deben tener un teléfono y un correo de contacto.')