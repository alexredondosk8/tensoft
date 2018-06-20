from django.db import models
from django.conf import settings
from datetime import datetime
import os
from .models import *
from RegUsuarios.models import *
from inmuebles.models import *

# Create your models here.
class Citas(models.Model):

    opt_estado_cita = (
        (1, 'Pendiente'),
        (2, 'Realizada'),
        (3, 'Cancelada')
    )


    id_cita = models.AutoField(primary_key=True)
    cedula = models.ForeignKey('RegUsuarios.Usuario', on_delete=models.CASCADE)
    codigo = models.ForeignKey('inmuebles.Inmueble', on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(default=datetime.now())
    fecha_cita = models.DateField()
    hora_cita = models.TimeField(null=True)
    hora_fin_cita = models.TimeField(null=True)
    estado_cita = models.IntegerField(choices=opt_estado_cita, default=1)
    comentarios = models.TextField(max_length=1000, null=True)


    def get_estado_cita(self):
        if self.estado_cita == 1:
            return 'Pendiente'
        elif self.estado_cita == 2:
            return 'Realizada'
        else:
            return 'Cancelada'

    def get_absolute_url(self):
        return "/citas/" + str(self.id_cita) + "/"
