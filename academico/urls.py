from django.urls import path
from . import views

urlpatterns = [
    path('registrar_calificacion/', views.registrar_calificacion, name='registrar_calificacion'),
]