# institucion/academico/forms.py
from django import forms
from .models import Asignacion, Materia, Curso, MaterialDidactico # ¡Importa MaterialDidactico!
from usuarios.models import Usuario

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['docente', 'materia', 'curso'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['docente'].queryset = Usuario.objects.filter(rol=Usuario.DOCENTE).order_by('username')
        self.fields['materia'].queryset = Materia.objects.all().order_by('grado__id', 'nombre')
        self.fields['curso'].queryset = Curso.objects.all().order_by('grado__id', 'nombre')
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                 field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        materia = cleaned_data.get("materia")
        curso = cleaned_data.get("curso")

        if materia and curso:
            if materia.grado != curso.grado:
                raise forms.ValidationError(
                    f"Error de grado: La materia '{materia}' ({materia.grado.nombre}) "
                    f"no coincide con el grado del curso '{curso}' ({curso.grado.nombre})."
                )
        return cleaned_data

# --- ¡ESTA ES LA CLASE QUE FALTABA! ---
class MaterialDidacticoForm(forms.ModelForm):
    class Meta:
        model = MaterialDidactico
        # El usuario solo llenará estos campos:
        fields = ['titulo', 'descripcion', 'archivo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}), # Hacemos la descripción un textarea
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos estilos de Bootstrap
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['archivo'].widget.attrs.update({'class': 'form-control'})