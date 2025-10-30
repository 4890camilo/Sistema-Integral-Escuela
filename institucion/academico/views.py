# institucion/academico/views.py

# --- Imports necesarios ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date 


# --- Modelos de esta app ---
from .models import Asignacion, Calificacion, Asistencia, Curso, Materia, MaterialDidactico
# --- Modelos de otras apps (Usuario) ---
from usuarios.models import Usuario 
# --- Formularios de esta app ---
from .forms import AsignacionForm, MaterialDidacticoForm

# ===============================================
# VISTAS PARA EL DOCENTE
# ===============================================

@login_required
def hub_calificaciones_view(request):
    """HUB: Muestra la lista de asignaciones para elegir dónde calificar."""
    if not request.user.rol == Usuario.DOCENTE: return redirect('dashboard')
    asignaciones = Asignacion.objects.filter(docente=request.user).order_by('curso__nombre')
    context = {
        'asignaciones': asignaciones,
        'titulo_hub': 'Ingresar Calificaciones',
        'subtitulo_hub': 'Selecciona la materia y curso que deseas calificar:',
        'url_destino': 'academico:ingresar_calificaciones'
    }
    return render(request, 'academico/hub_seleccion.html', context)

@login_required
def hub_asistencia_view(request):
    """HUB: Muestra la lista de asignaciones para elegir dónde tomar asistencia."""
    if not request.user.rol == Usuario.DOCENTE: return redirect('dashboard')
    asignaciones = Asignacion.objects.filter(docente=request.user).order_by('curso__nombre')
    context = {
        'asignaciones': asignaciones,
        'titulo_hub': 'Registrar Asistencia',
        'subtitulo_hub': 'Selecciona la materia y curso para tomar asistencia:',
        'url_destino': 'academico:registrar_asistencia'
    }
    return render(request, 'academico/hub_seleccion.html', context)

@login_required
def hub_material_view(request):
    """HUB: Muestra la lista de asignaciones para elegir dónde gestionar material."""
    if not request.user.rol == Usuario.DOCENTE: return redirect('dashboard')
    asignaciones = Asignacion.objects.filter(docente=request.user).order_by('curso__nombre')
    context = {
        'asignaciones': asignaciones,
        'titulo_hub': 'Material Didáctico',
        'subtitulo_hub': 'Selecciona la materia y curso para gestionar el material:',
        'url_destino': 'academico:gestionar_material'
    }
    return render(request, 'academico/hub_seleccion.html', context)

@login_required
def ingresar_calificaciones_view(request, pk):
    """ACCIÓN: Muestra la tabla para poner notas."""
    asignacion = get_object_or_404(Asignacion, pk=pk, docente=request.user)
    estudiantes_del_curso = asignacion.curso.estudiantes.filter(rol=Usuario.ESTUDIANTE).order_by('last_name', 'first_name')
    if request.method == 'POST':
        periodo = request.POST.get('periodo')
        if not periodo:
            messages.error(request, 'Debes especificar un Concepto de Calificación.')
        else:
            notas_guardadas = 0
            for estudiante in estudiantes_del_curso:
                nombre_input = f'nota_{estudiante.id}'
                nota_str = request.POST.get(nombre_input)
                if nota_str:
                    try:
                        nota_float = float(nota_str)
                        if 0 <= nota_float <= 100:
                            Calificacion.objects.update_or_create(
                                estudiante=estudiante, asignacion=asignacion, periodo=periodo,
                                defaults={'nota': nota_float}
                            )
                            notas_guardadas += 1
                        else:
                            messages.warning(request, f"Nota para {estudiante.username} ({nota_str}) fuera de rango (0-100). Ignorada.")
                    except ValueError:
                        messages.warning(request, f"Valor '{nota_str}' para {estudiante.username} no es número. Ignorado.")
            if notas_guardadas > 0: messages.success(request, f'Se guardaron/actualizaron {notas_guardadas} calificaciones para "{periodo}".')
            else: messages.info(request, 'No se ingresaron nuevas calificaciones.')
            return redirect('academico:ingresar_calificaciones', pk=asignacion.pk) 
    context = {'asignacion': asignacion, 'estudiantes_del_curso': estudiantes_del_curso}
    return render(request, 'academico/gestion_calificaciones.html', context)

@login_required
def registrar_asistencia_view(request, pk):
    """ACCIÓN: Muestra la tabla para tomar asistencia."""
    asignacion = get_object_or_404(Asignacion, pk=pk, docente=request.user)
    estudiantes_del_curso = asignacion.curso.estudiantes.filter(rol=Usuario.ESTUDIANTE).order_by('last_name', 'first_name')
    fecha_str = request.POST.get('fecha_asistencia', request.GET.get('fecha', date.today().isoformat()))
    try: fecha_seleccionada = date.fromisoformat(fecha_str)
    except ValueError: fecha_seleccionada = date.today()
    if request.method == 'POST':
        registros_guardados = 0
        for estudiante in estudiantes_del_curso:
            estado_input = request.POST.get(f'asistencia_{estudiante.id}')
            if estado_input:
                Asistencia.objects.update_or_create(
                    estudiante=estudiante, asignacion=asignacion, fecha=fecha_seleccionada,
                    defaults={'estado': estado_input}
                )
                registros_guardados += 1
        messages.success(request, f'Se guardaron {registros_guardados} registros de asistencia para el {fecha_seleccionada}.')
        return redirect(f"{request.path}?fecha={fecha_seleccionada.isoformat()}")
    asistencias_existentes = Asistencia.objects.filter(asignacion=asignacion, fecha=fecha_seleccionada)
    asistencia_hoy_map = {reg.estudiante.id: reg.estado for reg in asistencias_existentes}
    lista_estudiantes_con_estado = []
    for est in estudiantes_del_curso:
        estado_actual = asistencia_hoy_map.get(est.id, 'PRESENTE') 
        lista_estudiantes_con_estado.append({'estudiante': est, 'estado_actual': estado_actual})
    context = {
        'asignacion': asignacion, 'lista_estudiantes': lista_estudiantes_con_estado,
        'asistencia_estados': Asistencia.ESTADOS, 'fecha_seleccionada': fecha_seleccionada,
    }
    return render(request, 'academico/gestion_asistencia.html', context)

@login_required
def gestionar_material_view(request, pk):
    """ACCIÓN: Muestra la página para subir/ver material."""
    asignacion = get_object_or_404(Asignacion, pk=pk, docente=request.user)
    if request.method == 'POST':
        form = MaterialDidacticoForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False); material.asignacion = asignacion; material.save()
            messages.success(request, f"Se ha subido el material '{material.titulo}' correctamente.")
            return redirect('academico:gestionar_material', pk=asignacion.pk)
        else: messages.error(request, "Error al subir el material. Revisa el formulario.")
    materiales_existentes = MaterialDidactico.objects.filter(asignacion=asignacion).order_by('-fecha_subida')
    form = MaterialDidacticoForm()
    context = {'asignacion': asignacion, 'form': form, 'materiales': materiales_existentes}
    return render(request, 'academico/gestionar_material.html', context)

@login_required
def eliminar_material_view(request, pk):
    """ACCIÓN: Elimina un material."""
    material = get_object_or_404(MaterialDidactico, pk=pk, asignacion__docente=request.user)
    asignacion_pk = material.asignacion.pk
    if request.method == 'POST':
        material_titulo = material.titulo
        if material.archivo: material.archivo.delete(save=False) 
        material.delete()
        messages.success(request, f"Material '{material_titulo}' eliminado.")
        return redirect('academico:gestionar_material', pk=asignacion_pk)
    return redirect('academico:gestionar_material', pk=asignacion_pk)

# ===============================================
# VISTAS PARA EL ADMINISTRADOR
# ===============================================

@login_required
def listar_asignaciones_view(request):
    """ADMIN: Muestra la tabla de todas las asignaciones."""
    if not request.user.rol == Usuario.ADMINISTRATIVO: return redirect('dashboard') 
    asignaciones = Asignacion.objects.select_related('docente', 'materia', 'curso', 'curso__grado', 'materia__grado').order_by('curso__grado__id', 'curso__nombre', 'materia__nombre')
    context = {'asignaciones': asignaciones}
    return render(request, 'academico/listar_asignaciones.html', context)

@login_required
def crear_asignacion_view(request):
    """ADMIN: Muestra el formulario para crear una asignación."""
    if not request.user.rol == Usuario.ADMINISTRATIVO: return redirect('dashboard')
    if request.method == 'POST':
        form = AsignacionForm(request.POST)
        if form.is_valid():
            try: form.save(); messages.success(request, '¡Asignación creada correctamente!'); return redirect('academico:listar_asignaciones') 
            except Exception as e: messages.error(request, f'Error inesperado al guardar: {e}')
        else:
             messages.error(request, 'Error al crear la asignación. Revisa los campos.')
             context = {'form': form}
             return render(request, 'academico/crear_asignacion.html', context)
    else: form = AsignacionForm()
    context = {'form': form}
    return render(request, 'academico/crear_asignacion.html', context)

# ===============================================
# VISTAS PARA EL ESTUDIANTE (¡LAS QUE FALTABAN!)
# ===============================================

@login_required
def ver_calificaciones_view(request):
    """(RF-003) Muestra al estudiante sus propias calificaciones."""
    if not request.user.rol == Usuario.ESTUDIANTE:
        return redirect('dashboard')
        
    calificaciones = Calificacion.objects.filter(
        estudiante=request.user
    ).order_by('asignacion__materia__nombre', '-fecha') # Ordena por materia y fecha

    context = {
        'calificaciones': calificaciones,
        'estudiante': request.user
    }
    return render(request, 'academico/ver_calificaciones.html', context)

@login_required
def ver_asistencia_view(request):
    """(RF-006) Muestra al estudiante su propio historial de asistencia."""
    if not request.user.rol == Usuario.ESTUDIANTE:
        return redirect('dashboard')
        
    asistencias = Asistencia.objects.filter(
        estudiante=request.user
    ).order_by('-fecha', 'asignacion__materia__nombre') # Ordena por fecha más reciente

    context = {
        'asistencias': asistencias,
        'estudiante': request.user
    }
    return render(request, 'academico/ver_asistencia.html', context)

@login_required
def ver_material_view(request):
    """(RF-009) Muestra al estudiante el material de su curso."""
    if not request.user.rol == Usuario.ESTUDIANTE:
        return redirect('dashboard')
    
    # 1. Busca el curso del estudiante (ej: "Décimo A")
    curso_estudiante = request.user.curso
    
    materiales = None
    if curso_estudiante:
        # 2. Busca todo el material didáctico que haya sido subido
        #    para CUALQUIER asignación de ESE curso.
        materiales = MaterialDidactico.objects.filter(
            asignacion__curso=curso_estudiante
        ).select_related(
            'asignacion__materia', 'asignacion__docente'
        ).order_by('asignacion__materia__nombre', '-fecha_subida')
        # El .select_related() optimiza la consulta para que también traiga
        # los datos de la materia y el docente en un solo viaje a la BD.

    context = {
        'materiales': materiales, # La lista de materiales (o None)
        'curso_estudiante': curso_estudiante, # El objeto Curso (o None)
        'estudiante': request.user
    }
    return render(request, 'academico/ver_material.html', context)