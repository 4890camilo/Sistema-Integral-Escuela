
from django.db import models
from usuarios.models import Usuario

class Pago(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'ESTUDIANTE'}, related_name='pagos_como_estudiante')
    administrativo = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'rol': 'ADMINISTRATIVO'}, related_name='pagos_como_administrativo')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    estado = models.CharField(max_length=20, choices=[('PENDIENTE', 'Pendiente'), ('PAGADO', 'Pagado')])
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"{self.estudiante.username} - {self.monto} ({self.estado})"