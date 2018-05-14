from django.db import models

# Gestión de clientes (Dueños de casa, Apartamento o Locales)
# - Registrar clientes (los clientes deben poder poder crear su propia cuenta
#   donde el login debe ser el correo electronico y debe tener validación Captcha
#   Captcha).
# - Actualizar datos del clientes

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.CharField(max_length=254, primary_key=True)
    telefono = models.CharField(max_length=7)
    celular = models.CharField(max_length=10)
