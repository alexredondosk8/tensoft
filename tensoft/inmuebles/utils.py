from .models import *

def get_lista_inmuebles_activos(usuario):
    if usuario.is_superuser:
        return Inmueble.objects.filter(estado=True).order_by('fecha_registro')
    else:
        return Inmueble.objects.filter(estado=True).order_by('fecha_registro')

    return []
