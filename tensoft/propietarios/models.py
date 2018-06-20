from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import User

class Propietario(models.Model):

    id_propietario = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=80)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80)
    telefono = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    estado = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, null=True)

    def get_absolute_url(self):
        return "/propietarios/" + str(self.id_propietario) + "/actualizar"

# Create your models here.
