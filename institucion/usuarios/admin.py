
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'telefono', 'direccion')}),
    )

admin.site.register(Usuario, UsuarioAdmin)