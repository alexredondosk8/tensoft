from .models import *

def get_lista_citas(usuario, estado):
    if usuario.is_superuser:
        return Citas.objects.filter(estado=True, estado_cita=estado).order_by('fecha_registro')
    else:
        return Citas.objects.filter(estado=True, estado_cita=estado).order_by('fecha_registro')

    return []
