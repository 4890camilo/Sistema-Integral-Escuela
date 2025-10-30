# institucion/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from academico.models import Curso

# --- 1. TU FORMULARIO DE REGISTRO PÚBLICO (SIN CAMBIOS) ---
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol', 'telefono', 'direccion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que 'rol' use las opciones de tu modelo
        self.fields['rol'].widget = forms.Select(choices=Usuario.ROLES)


# --- 2. FORMULARIO DEL ADMIN PARA CREAR PERSONAL (CON CAMPO CURSO Y WIDGET DIRECCION) ---
class PersonalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all().order_by('grado__id', 'nombre'), # Ordena los cursos
        required=False, # ¡Importante! No es obligatorio
        label="Curso Asignado (Solo Estudiantes)"
    )

    class Meta:
        model = Usuario
        # Añadimos 'curso' a la lista de campos
        fields = [
            'username', 'password', 'first_name', 'last_name', 'rol',
            'email', 'correo', 'telefono', 'direccion', 'curso', # <-- Campo añadido
        ]
        # Hacemos que el widget de 'direccion' sea un Textarea con 3 filas
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos estilos de Bootstrap
        for field_name, field in self.fields.items():
            # Asignamos clases según el tipo de widget
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'}) # Ya tiene rows de Meta
            elif not isinstance(field.widget, forms.CheckboxInput): # Evita Checkbox si lo hubiera
                field.widget.attrs.update({'class': 'form-control'})

        # El admin solo debe poder crear estos roles (excepto Admin)
        todos_los_roles = list(Usuario.ROLES)
        roles_para_admin = [('', '---------')]
        for valor, etiqueta in todos_los_roles:
            if valor != Usuario.ADMINISTRATIVO:
                roles_para_admin.append((valor, etiqueta))
        self.fields['rol'].choices = roles_para_admin

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])

        # Si no es estudiante, nos aseguramos de que el curso quede vacío
        if self.cleaned_data['rol'] != Usuario.ESTUDIANTE:
            usuario.curso = None
        else: # Si es estudiante, se asigna el curso, pero puede ser None si no lo seleccionó
            usuario.curso = self.cleaned_data.get('curso', None) # Asignamos el curso seleccionado

        # Asignamos is_staff si es Docente
        if self.cleaned_data['rol'] == Usuario.DOCENTE:
            usuario.is_staff = True
        else:
            usuario.is_staff = False

        if commit:
            usuario.save()
        return usuario


# --- 3. FORMULARIO DEL ADMIN PARA EDITAR PERSONAL (CON CAMPO CURSO) ---
class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Incluimos 'curso' en la lista de campos
        fields = [
            'first_name',
            'last_name',
            'rol',
            'email',      # Email institucional
            'correo',     # Email personal
            'telefono',
            'direccion',
            'is_active',  # Para activar/desactivar cuentas
            'curso',      # <-- Campo añadido aquí también
        ]
        # Ajustamos el widget de direccion también para editar
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos estilos de Bootstrap
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                 field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                 field.widget.attrs.update({'class': 'form-control'}) # Ya tiene rows de Meta
            elif not isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs.update({'class': 'form-control'})

        # Al editar, dejamos que el admin cambie a CUALQUIER rol
        self.fields['rol'].choices = [('', '---------')] + list(Usuario.ROLES)

        # Ocultamos o mostramos el campo 'curso' según el rol actual del usuario
        instance = kwargs.get('instance')
        if instance and instance.rol != Usuario.ESTUDIANTE:
            self.fields['curso'].widget = forms.HiddenInput()
            self.fields['curso'].required = False
        elif 'curso' in self.fields: # Si es estudiante, nos aseguramos que sea un select visible
             self.fields['curso'].widget = forms.Select(attrs={'class': 'form-select'}) # Asegura que sea Select visible
             # Puedes decidir si el curso es obligatorio al editar un estudiante
             # self.fields['curso'].required = True