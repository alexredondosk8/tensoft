from django.db import models
from django.conf import settings
import os

class Propietario(models.Model):

    id_propietario = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=80)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80)
    telefono = models.CharField(max_length=80)
    email = models.CharField(max_length=80)


# Create your models here.
