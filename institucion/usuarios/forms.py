# institucion/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

# --- 1. TU FORMULARIO DE REGISTRO PÚBLICO (SIN CAMBIOS) ---
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol', 'telefono', 'direccion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].widget = forms.Select(choices=Usuario.ROLES) 


# --- 2. FORMULARIO DEL ADMIN PARA CREAR PERSONAL ---
class PersonalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Usuario
        fields = [
            'username', 'password', 'first_name', 'last_name', 'rol',
            'email', 'correo', 'telefono', 'direccion',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        todos_los_roles = list(Usuario.ROLES)
        roles_para_admin = [('', '---------')]
        for valor, etiqueta in todos_los_roles:
            if valor != 'ADMINISTRATIVO':
                roles_para_admin.append((valor, etiqueta))
        
        self.fields['rol'].choices = roles_para_admin

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        
        if self.cleaned_data['rol'] == 'DOCENTE':
            usuario.is_staff = True
        else:
            usuario.is_staff = False
        
        if commit:
            usuario.save()
        return usuario

# --- 3. ¡NUEVO! FORMULARIO DEL ADMIN PARA EDITAR PERSONAL ---
class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # No incluimos 'username' (no se debe cambiar)
        # No incluimos 'password' (se maneja por separado)
        fields = [
            'first_name',
            'last_name',
            'rol',
            'email',      # Email institucional
            'correo',     # Email personal
            'telefono',
            'direccion',
            'is_active',  # Para activar/desactivar cuentas
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos estilos de Bootstrap
        for field_name, field in self.fields.items():
            # No aplicamos 'form-control' a los checkboxes
            if not isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs.update({'class': 'form-control'})
        
        # Al editar, dejamos que el admin cambie a CUALQUIER rol
        self.fields['rol'].choices = [('', '---------')] + list(Usuario.ROLES)