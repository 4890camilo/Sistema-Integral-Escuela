# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'index.html', {'error': 'Usuario o contraseña incorrectos' if 'error' in request.GET else None})

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
    rol = request.user.rol  # Obtiene el rol del usuario desde el modelo Usuario
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
        template = 'usuarios/panel_admin.html'  # Predeterminado si no coincide
    return render(request, template, {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')