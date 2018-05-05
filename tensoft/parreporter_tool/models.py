from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class ReportarInconveniente(models.Model):
    opt_prioridades = (
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta')
    )

    prioridad = models.IntegerField(choices=opt_prioridades)
    mensaje = models.TextField(max_length=1000)
    imagen = models.ImageField(null=True, upload_to='reportes')
    desarrollador = models.ForeignKey(User)
    fecha_generacion = models.DateTimeField(default=datetime.now())
    fecha_cierre = models.DateTimeField(null=True)
    observaciones = models.TextField(max_length=1000, null=True)
