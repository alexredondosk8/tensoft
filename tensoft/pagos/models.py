from django.db import models
from datetime import datetime

# Create your models here.
class PagosInmueble(models.Model):

    opt_tipo_pago = (
        (1, 'Alquiler'),
        (2, 'Venta'),
        #(3, 'Alquiler/Venta')
    )

    opt_tipo_moneda = (
        (1, 'Peso Colombiano-COP'),
        (2, 'Dólar estadounidense-USD'),
        (3, 'Euro-EUR')
    )

    numero_factura = models.AutoField(primary_key=True)
    periodo_inicio_factura = models.DateField(null=True)
    periodo_final_factura = models.DateField(null=True)
    fecha_emision_factura = models.DateTimeField(auto_now_add=True)
    fecha_limite_pago = models.DateField()
    fecha_pago = models.DateTimeField(null=True)
    valor_pago = models.FloatField()
    tipo_moneda = models.IntegerField(choices=opt_tipo_moneda)
    tipo_pago = models.IntegerField(choices=opt_tipo_pago)
    pagada = models.BooleanField(default=False)
    diferencia_dias_pago = models.IntegerField(null=True)
    usuario = models.ForeignKey('RegUsuarios.Usuario')
    inmueble = models.ForeignKey('inmuebles.Inmueble')
    estado_obj = models.BooleanField(default=True)

    """def __str__(self):
        return "Factura número " + str(self.numero_factura)"""

    def get_tipo_pago(self):
        if self.tipo_pago == 1:
            return 'Alquiler'
        elif self.tipo_pago == 2:
            return 'Venta'
        else:
            return 'Transacción desconocida'

    def get_tipo_moneda(self):
        if self.tipo_moneda == 1:
            return 'COP'
        elif self.tipo_moneda == 2:
            return 'USD'
        else:
            return 'EUR'

    def get_estado_pago(self):
        if self.pagada == True:
            return 'Factura pagada'
        else:
            return 'Factura pendiente de pago'

    def is_factura_pagada(self):
        if self.fecha_pago is not None:
            return True
        else:
            return False

    def is_factura_mora(self):
        if datetime.now().date() > self.fecha_limite_pago and self.pagada == False:
            return True
        else:
            return False

    def is_factura_pagada_a_tiempo(self):
        if self.is_factura_pagada():
            if self.diferencia_dias_pago < 0:
                return False
            else:
                return True

    def get_dias_mora(self):
        if self.pagada:
            if self.fecha_pago.date() <= self.fecha_limite_pago:
                return 0
            else:
                return (self.fecha_pago.date() - self.fecha_limite_pago).days
        else:
            if self.fecha_limite_pago < datetime.now().date():
                return (datetime.now().date() - self.fecha_limite_pago).days
            else:
                return 0
