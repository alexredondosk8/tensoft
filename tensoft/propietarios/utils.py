import os
from subprocess import call
from .models import *

def get_lista_propietarios(usuario):
    # if usuario.is_superuser:
    #     return Inmueble.objects.filter(estado=True, estado_operacional=estado).order_by('fecha_registro')
    # else:
    #     return Inmueble.objects.filter(estado=True, estado_operacional=estado).order_by('fecha_registro')
    return Propietario.objects.all()

    #return []