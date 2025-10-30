# institucion/usuarios/views.py

# --- Imports necesarios ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# --- Modelos ---
from .models import Usuario # Importa tu modelo de Usuario
from academico.models import Asignacion, Calificacion, Asistencia # Importa modelos de academico

# --- Formularios ---
from .forms import UsuarioCreationForm, PersonalForm, PersonalEditForm
# (Asegúrate de que 'academico.forms' se importe en 'academico.views' si lo moviste)


# --- VISTAS DE AUTENTICACIÓN Y CRUD (TU CÓDIGO) ---

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    error_msg = 'Usuario o contraseña incorrectos' if request.method == 'POST' else None
    return render(request, 'index.html', {'error': error_msg})

def register_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# --- VISTA DE DASHBOARD (¡LA PARTE CORREGIDA!) ---

@login_required
def dashboard(request):
    rol = request.user.rol
    context = {'user': request.user} # Solo pasamos el usuario
    
    if rol == Usuario.ADMINISTRATIVO:
        template = 'usuarios/panel_admin.html'
    
    # --- ¡SIMPLIFICADO! ---
    # Ya no busca asignaciones. Solo muestra el panel con los cuadritos.
    elif rol == Usuario.DOCENTE:
        template = 'usuarios/panel_docente.html' 
    # --- FIN DE LA SIMPLIFICACIÓN ---
    
    elif rol == Usuario.ESTUDIANTE:
        template = 'usuarios/panel_estudiante.html' 
    elif rol == Usuario.PADRES:
         template = 'usuarios/panel_padres.html'
    else:
        template = 'usuarios/panel_generico.html' 
        
    return render(request, template, context) # Solo envía el 'user'

@login_required
def registrar_personal_view(request):
    if not request.user.rol == Usuario.ADMINISTRATIVO:
        return redirect('dashboard') 
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, '¡Usuario registrado correctamente!')
            return redirect('consultar_personal')
        else:
             messages.error(request, 'Error al registrar. Revisa los campos.')
    else:
        form = PersonalForm()
    return render(request, 'usuarios/registrar_personal.html', {'form': form})

@login_required
def consultar_personal_view(request):
    if not request.user.rol == Usuario.ADMINISTRATIVO:
        return redirect('dashboard')
    lista_personal = Usuario.objects.filter(is_superuser=False).order_by('last_name')
    return render(request, 'usuarios/consultar_personal.html', {'personal': lista_personal})

@login_required
def editar_personal_view(request, pk):
    if not request.user.rol == Usuario.ADMINISTRATIVO:
        return redirect('dashboard')
    usuario_a_editar = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = PersonalEditForm(request.POST, instance=usuario_a_editar)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario actualizado!')
            return redirect('consultar_personal')
    else:
        form = PersonalEditForm(instance=usuario_a_editar)
    return render(request, 'usuarios/editar_personal.html', {'form': form, 'usuario_a_editar': usuario_a_editar})

@login_required
def eliminar_personal_view(request, pk):
    if not request.user.rol == Usuario.ADMINISTRATIVO:
        return redirect('dashboard')
    if request.method == 'POST':
        usuario_a_eliminar = get_object_or_404(Usuario, pk=pk)
        if not usuario_a_eliminar.is_superuser:
            usuario_a_eliminar.delete()
            messages.success(request, 'Usuario eliminado.')
        return redirect('consultar_personal')
    return redirect('consultar_personal')