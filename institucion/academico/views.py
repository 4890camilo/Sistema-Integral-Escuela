# academico/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Calificacion
from usuarios.models import Usuario

def is_docente(user):
    return user.is_authenticated and user.rol == 'DOCENTE'

@login_required
@user_passes_test(is_docente)
def registrar_calificacion(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        curso = request.POST.get('curso')
        nota = request.POST.get('nota')
        periodo = request.POST.get('periodo')
        if estudiante_id and curso and nota and periodo:
            Calificacion.objects.create(
                estudiante_id=estudiante_id, docente=request.user, curso=curso, nota=float(nota), periodo=periodo
            )
            return redirect('dashboard')
    usuarios = Usuario.objects.filter(rol='ESTUDIANTE')
    return render(request, 'academico/registrar_calificacion.html', {'usuarios': usuarios})