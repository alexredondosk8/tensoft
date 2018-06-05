import os
from subprocess import call
from .models import *

def get_lista_inmuebles(usuario, estado):
    if usuario.is_superuser:
        return Inmueble.objects.filter(estado=True, estado_operacional=estado).order_by('fecha_registro')
    else:
        return Inmueble.objects.filter(estado=True, estado_operacional=estado).order_by('fecha_registro')

    return []

def insertar_departamentos_municipios(schema_name):
    archivo_dep = open("acciones_previas/departamentos.txt")
    departamentos = archivo_dep.readlines()

    archivo_mun = open("acciones_previas/municipios.txt")
    municipios = archivo_mun.readlines()

    str_insert_dep = 'INSERT INTO ' + schema_name + ".inmuebles_departamento values "
    for departamento in departamentos:
        str_insert_dep += departamento

    str_insert_mun = 'INSERT INTO ' + schema_name + '.inmuebles_municipio ("id_municipio", "departamento_id", "nombre")'
    str_insert_mun += " values "
    for municipio in municipios:
        str_insert_mun += municipio

    file_insert = open("acciones_previas/script_insert_dep_mun.sql", "w")

    file_insert.write(str_insert_dep)
    file_insert.write(str_insert_mun)

    file_insert.close()

    os.system("PGPASSWORD=univalle psql -U univalle -d inmobiliarias_tensoft -h localhost -p 5432 -f acciones_previas/script_insert_dep_mun.sql")

def get_municipios_dpto():
    municipios = Municipio.objects.all().order_by("nombre")
    lista_tuplas = []
    for municipio in municipios:
        departamento = Departamento.objects.get(id_departamento=municipio.departamento_id)
        lista_tuplas.append((municipio.id_municipio, municipio.nombre + " / " + departamento.nombre))

    return lista_tuplas
