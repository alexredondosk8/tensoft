from django.db import models, connection, IntegrityError
from django.core.management import call_command
from django.contrib.auth.models import User
from datetime import datetime
from django_tenants.models import TenantMixin, DomainMixin
from tenant_schemas.utils import get_public_schema_name, schema_exists

from tenant_schemas.postgresql_backend.base import _check_schema_name

# Gestión de clientes (Dueños de casa, Apartamento o Locales)
# - Registrar clientes (los clientes deben poder poder crear su propia cuenta
#   donde el login debe ser el correo electronico y debe tener validación Captcha
#   Captcha).
# - Actualizar datos del clientes

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, primary_key=True)
    correo = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=7)
    celular = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre + " " + self.apellidos
