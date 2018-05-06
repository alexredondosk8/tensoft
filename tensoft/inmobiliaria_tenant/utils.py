from .models import Inmobiliaria, Cliente

def lista_inmobiliarias_pendientes_alta(usuario):

    if usuario.is_superuser:
        pendientes_alta = Inmobiliaria.objects.filter(estado=False, fecha_revision=None).order_by('fecha_registro')

    else:
        pendientes_alta = Inmobiliaria.objects.filter(estado=False, fecha_revision=None,
            representante=Cliente.objects.get(usuario=usuario)).order_by('fecha_registro')

    return pendientes_alta

def lista_inmobiliarias_pendientes_baja(usuario):
    if usuario.is_superuser:
        pendientes_baja = Inmobiliaria.objects.filter(estado=True, solicitud_baja=True, fecha_baja__isnull=True).order_by('fecha_solicitud_baja')

    else:
        pendientes_baja = Inmobiliaria.objects.filter(estado=True, solicitud_baja=True,
            representante__usuario=usuario).order_by('fecha_solicitud_baja')
    return pendientes_baja

def lista_inmobiliarias_activas(usuario):
    if usuario.is_superuser:
        lista = Inmobiliaria.objects.filter(estado=True).exclude(representante__usuario=usuario).order_by('fecha_registro')
    else:
        lista = Inmobiliaria.objects.filter(estado=True, representante__usuario=usuario).order_by('fecha_registro')

    return lista

def lista_inmobiliarias_inactivas(usuario):
    if usuario.is_superuser:
        lista = Inmobiliaria.objects.filter(fecha_baja__isnull=False).order_by('fecha_baja')
    else:
        lista = Inmobiliaria.objects.filter(estado=True, representante__usuario=usuario).order_by('fecha_registro')

    return lista

def procesar_schema_name(nombre):
    nombre = nombre.replace("/", "")
    nombre = nombre.replace("-", "")
    nombre = nombre.replace("_", "")

    return nombre
