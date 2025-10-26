from django.urls import path
from . import views

urlpatterns = [
    path('validar_pago/', views.validar_pago, name='validar_pago'),
]