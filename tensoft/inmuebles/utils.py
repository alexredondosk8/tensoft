from .models import *

def get_lista_inmuebles(usuario, estado):
    if usuario.is_superuser:
        return Inmueble.objects.filter(estado=True, estado_operacional=estado).order_by('fecha_registro')
    else:
        return Inmueble.objects.filter(estado=True, estado_operacional=estado).order_by('fecha_registro')

    return []
