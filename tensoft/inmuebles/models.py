from django.db import models
from django.conf import settings
import os
# from propietarios.models import propietario

def generate_upload_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT+"/inmuebles/"+str(instance.codigo.codigo)+"/"+filename)

# Create your models here.
class Inmueble(models.Model):
    opt_tipo_inmueble = (
        (1, 'Casa'),
        (2, 'Apartamento'),
        (3, 'Local')
    )

    opt_tipo_parqueadero = (
        (1, 'Cubierto'),
        (2, 'Semicubierto'),
        (3, 'Comunal')
    )

    opt_tipo_transaccion = (
        (1, 'Alquiler'),
        (2, 'Venta'),
        (3, 'Alquiler/Venta')
    )

    opt_tipo_moneda = (
        (1, 'Peso Colombiano-COP'),
        (2, 'Dólar estadounidense-USD'),
        (3, 'Euro-EUR')
    )
    codigo = models.AutoField(primary_key=True)
    tipo_inmueble = models.IntegerField(choices=opt_tipo_inmueble)
    tipo_transaccion = models.IntegerField(choices=opt_tipo_transaccion)
    valor = models.FloatField()
    tipo_moneda = models.IntegerField(choices=opt_tipo_moneda)
    area = models.FloatField()
    numero_habitaciones = models.IntegerField()
    numero_baños = models.IntegerField()
    parqueadero = models.BooleanField()
    tipo_parqueadero = models.IntegerField(choices=opt_tipo_parqueadero, null=True, blank=True)
    parqueadero_visitantes = models.BooleanField()
    estrato = models.IntegerField()
    barrio = models.CharField(max_length=45)
    direccion = models.CharField(max_length=80)
    estado = models.BooleanField(default=True)
    descripcion = models.TextField(max_length=1000)
    #propietario = models.ForeignKey('propietario')

class FotosInmueble(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='images')
    imagen = models.ImageField(upload_to=generate_upload_path)
