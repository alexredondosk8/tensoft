from django.db import models, connection
from django.core.management import call_command
from django.contrib.auth.models import User
from datetime import datetime
from django_tenants.models import TenantMixin, DomainMixin
from tenant_schemas.utils import get_public_schema_name, schema_exists

from tenant_schemas.postgresql_backend.base import _check_schema_name

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, primary_key=True)
    correo = models.EmailField(max_length=254)
    usuario = models.ForeignKey(User, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos

class Inmobiliaria(TenantMixin):
    nombre = models.CharField(max_length=100)
    representante = models.ForeignKey(Cliente)
    estado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(default=datetime.now())
    fecha_revision = models.DateTimeField(null=True)
    solicitud_baja = models.BooleanField(default=False)
    fecha_solicitud_baja = models.DateTimeField(null=True)
    fecha_baja = models.DateTimeField(null=True)

    auto_create_schema = False

    class Meta:
        ordering = ['fecha_registro']

    def __str__(self):
        return self.nombre

    def get_estado(self):
        if self.estado == False and self.fecha_revision is not None and self.fecha_baja is not None:
            return 'Cerrada'
        if self.estado == False and self.fecha_revision is not None:
            return "Rechazada"
        elif self.estado == False:
            return "En espera de aprobación"
        elif self.estado == True and self.solicitud_baja == True:
            return "En espera de aprobación de cierre"
        else:
            return "Activa"

    def get_revision(self):
        if self.fecha_revision == None:
            return 'Pendiente'
        else:
            return self.fecha_revision
    def get_baja(self):
        if self.solicitud_baja == True:
            return 'Sí'
        else:
            return 'No'
    def get_fecha_baja(self):
        if self.fecha_baja == None and self.solicitud_baja == True:
            return 'Pendiente de aprobación de cierre'
        elif self.fecha_baja == None:
            return 'N/A'
        elif self.fecha_baja is not None and self.solicitud_baja == True:
            return self.fecha_baja


class Domain(DomainMixin):
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.domain
