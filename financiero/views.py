# financiero/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pago
from usuarios.models import Usuario

def is_administrativo(user):
    return user.is_authenticated and user.rol == 'ADMINISTRATIVO'

@login_required
@user_passes_test(is_administrativo)
def validar_pago(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        monto = request.POST.get('monto')
        fecha_pago = request.POST.get('fecha_pago')
        estado = request.POST.get('estado')
        if estudiante_id and monto and fecha_pago and estado:
            Pago.objects.create(
                estudiante_id=estudiante_id, administrativo=request.user, monto=float(monto), fecha_pago=fecha_pago, estado=estado
            )
            return redirect('dashboard')
    usuarios = Usuario.objects.filter(rol='ESTUDIANTE')
    return render(request, 'financiero/validar_pago.html', {'usuarios': usuarios})