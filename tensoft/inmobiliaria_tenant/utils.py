from .models import Inmobiliaria, Cliente

def lista_inmobiliarias_pendientes(usuario):

    if usuario.is_superuser:
        pendientes_alta = Inmobiliaria.objects.filter(estado=False, fecha_revision=None).order_by('fecha_registro')
        #pendientes_baja = Inmobiliaria.objects.filter(solicitud_baja=True, fecha_baja__isnull=True)

    else:
        pendientes_alta = Inmobiliaria.objects.filter(estado=False, fecha_revision=None,
            representante=Cliente.objects.get(usuario=usuario)).order_by('fecha_registro')
        """pendientes_baja = Inmobiliaria.objects.filter(solicitud_baja=True, fecha_baja__isnull=True,
            representante=Cliente.objects.get(usuario=usuario))"""

    return {'alta': pendientes_alta,
            #'baja': pendientes_baja
            }

def procesar_schema_name(nombre):
    nombre = nombre.replace("/", "")
    nombre = nombre.replace("-", "")
    nombre = nombre.replace("_", "")

    return nombre
