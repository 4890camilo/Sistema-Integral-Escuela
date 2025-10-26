# institucion/usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Importamos los TRES formularios
from .forms import UsuarioCreationForm, PersonalForm, PersonalEditForm
# Importamos el modelo para las consultas
from .models import Usuario

# --- TUS VISTAS EXISTENTES (LOGIN, REGISTER, DASHBOARD, LOGOUT) ---
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

@login_required
def dashboard(request):
    rol = request.user.rol
    if rol == 'ADMINISTRATIVO':
        template = 'usuarios/panel_admin.html'
    elif rol == 'DOCENTE':
        template = 'usuarios/panel_docente.html' 
    elif rol == 'ESTUDIANTE':
        template = 'usuarios/panel_estudiante.html' 
    elif rol == 'FINANCIERO':
        template = 'usuarios/panel_financiero.html' 
    elif rol == 'PADRES':
        template = 'usuarios/panel_padres.html' 
    else:
        template = 'usuarios/panel_generico.html' 
    return render(request, template, {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login') # Asegúrate de tener una URL con name='login'

# --- ¡NUEVAS VISTAS PARA EL CRUD DE PERSONAL! ---

# 1. VISTA PARA REGISTRAR (LA QUE YA HICIMOS)
@login_required
def registrar_personal_view(request):
    if not request.user.rol == 'ADMINISTRATIVO':
        return redirect('dashboard') 
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('consultar_personal') # Redirige a la tabla
    else:
        form = PersonalForm()
    return render(request, 'usuarios/registrar_personal.html', {'form': form})

# 2. ¡NUEVA VISTA! PARA VER LA TABLA DE PERSONAL
@login_required
def consultar_personal_view(request):
    if not request.user.rol == 'ADMINISTRATIVO':
        return redirect('dashboard')
    
    lista_personal = Usuario.objects.filter(is_superuser=False).order_by('last_name')
    
    return render(request, 'usuarios/consultar_personal.html', {
        'personal': lista_personal
    })

# 3. ¡NUEVA VISTA! PARA EDITAR UN USUARIO
@login_required
def editar_personal_view(request, pk): # 'pk' es el ID del usuario
    if not request.user.rol == 'ADMINISTRATIVO':
        return redirect('dashboard')
    
    usuario_a_editar = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = PersonalEditForm(request.POST, instance=usuario_a_editar)
        if form.is_valid():
            form.save()
            return redirect('consultar_personal') # Volvemos a la lista
    else:
        form = PersonalEditForm(instance=usuario_a_editar)
    
    return render(request, 'usuarios/editar_personal.html', {
        'form': form,
        'usuario_a_editar': usuario_a_editar
    })

# 4. ¡NUEVA VISTA! PARA ELIMINAR UN USUARIO
@login_required
def eliminar_personal_view(request, pk):
    if not request.user.rol == 'ADMINISTRATIVO':
        return redirect('dashboard')
    
    if request.method == 'POST':
        usuario_a_eliminar = get_object_or_404(Usuario, pk=pk)
        if not usuario_a_eliminar.is_superuser:
            usuario_a_eliminar.delete()
        return redirect('consultar_personal')
    
    return redirect('consultar_personal')