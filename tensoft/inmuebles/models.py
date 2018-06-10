from django.db import models
from django.conf import settings
from datetime import datetime
import os
# from propietarios.models import propietario

def generate_upload(instance, filename):
    return "inmuebles/"+str(instance.codigo.codigo)+"/"+filename

# Create your models here.
class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    id_municipio = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento)

    def __str__(self):
        return self.nombre

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
        #(3, 'Alquiler/Venta')
    )

    opt_tipo_moneda = (
        (1, 'Peso Colombiano-COP'),
        (2, 'Dólar estadounidense-USD'),
        (3, 'Euro-EUR')
    )

    opt_estado_operacional = (
        (1, 'Disponible'), # se muestra el inmueble a clientes
        (2, 'Ocupado'),     # no se muestra el inmueble a clientes porque alguien lo alquiló o compró
        (3, 'No disponible')# no se muestra el inmueble a clientes por otros motivos
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
    municipio = models.ForeignKey(Municipio, null=True)
    estado = models.BooleanField(default=True)
    descripcion = models.TextField(max_length=1000)
    fecha_registro = models.DateTimeField(default=datetime.now())
    estado_operacional = models.IntegerField(choices=opt_estado_operacional, default=1)
    propietario = models.ForeignKey('propietarios.Propietario', null=True)
    arrendatario = models.ForeignKey('RegUsuarios.Usuario', null=True)

    def get_tipo_inmueble(self, capitalize=True):
        if self.tipo_inmueble == 1:
            if capitalize:
                return 'Casa'
            else:
                return 'casa'
        elif self.tipo_inmueble == 2:
            if capitalize:
                return 'Apartamento'
            else:
                return 'apartamento'
        else:
            if capitalize:
                return 'Local'
            else:
                return 'local'

    def get_tipo_transaccion(self):
        if self.tipo_transaccion == 1:
            return 'Alquiler'
        else:
            return 'Venta'

    def get_tipo_moneda(self):
        if self.tipo_moneda == 1:
            return 'COP'
        elif self.tipo_moneda == 2:
            return 'USD'
        else:
            return 'EUR'

    def get_parqueadero(self):
        if self.parqueadero == True:
            return 'Sí'
        else:
            return 'No'

    def get_tipo_parqueadero(self):
        if self.get_parqueadero() == 'No':
            return 'N/A'
        elif self.tipo_parqueadero == 1:
            return 'Cubierto'
        elif self.tipo_parqueadero == 2:
            return 'Semicubierto'
        else:
            return 'Comunal'

    def get_parqueadero_visitantes(self):
        if self.parqueadero_visitantes == True:
            return 'Sí'
        else:
            return 'No'

    def get_estado_operacional(self):
        if self.estado_operacional == 1:
            return 'Disponible'
        elif self.estado_operacional == 2:
            return 'Ocupado'
        else:
            return 'No disponible'

    def get_absolute_url(self):
        return "/inmuebles/" + str(self.codigo) + "/"

class FotosInmueble(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='images')
    imagen = models.ImageField(upload_to=generate_upload)
