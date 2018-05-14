from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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
    usuario = models.ForeignKey(User, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos
