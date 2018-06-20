from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
import simplejson as json
from django.template import Context
from django.template.loader import get_template
from weasyprint import HTML, CSS
from datetime import datetime, timedelta
from inmobiliaria_tenant.models import *
from inmuebles.models import *
from propietarios.models import *
from pagos.models import *
from inmobiliaria_tenant.utils import actualizar_edad_clientes

# Create your views here.


def pdf_generation(request, template_src, context_dict, file_name):
    html_template = get_template(template_src)
    #context = Context(context_dict)
    print(context_dict)
    pdf_file = HTML(string=html_template.render(context_dict)).write_pdf(stylesheets=[CSS('static/build/css/style.css')])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s"' % file_name
    return response

class ReporteListaInmueblesEstado(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super(ReporteListaInmueblesEstado, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        formato = kwargs['formato']
        estado = int(kwargs['id'])

        context['inmuebles'] = Inmueble.objects.filter(estado_operacional=estado).order_by('-fecha_registro')
        context['campos'] = [
            'Código',
            'Fecha de registro',
            'Área',
            'Barrio',
            'Municipio',
        ]

        if formato == 'pdf':
            context['exportar'] = True
        else:
            context['exportar'] = False

        if formato == 'pdf':
            return pdf_generation(request, "reportes/lista_inmuebles(pdf).html", context, "lista_inmuebles.pdf")

        return render(request, "inmuebles/lista_inmuebles.html", context)

class ReporteListaInmueblesTipo(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super(ReporteListaInmueblesTipo, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        formato = kwargs['formato']
        estado = int(kwargs['id'])

        context['inmuebles'] = Inmueble.objects.filter(tipo_inmueble=estado).order_by('-fecha_registro')
        context['campos'] = [
            'Código',
            'Fecha de registro',
            'Área',
            'Barrio',
            'Municipio',
        ]

        if formato == 'pdf':
            context['exportar'] = True
        else:
            context['exportar'] = False

        if formato == 'pdf':
            return pdf_generation(request, "reportes/lista_inmuebles(pdf).html", context, "lista_inmuebles.pdf")

        return render(request, "inmuebles/lista_inmuebles.html", context)

class ReporteSexoClientesRegistrados(TemplateView):
    template_name = "reportes/sexo.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteSexoClientesRegistrados, self).get_context_data(**kwargs)

        json_info = [
            {
                'sexo': 'Masculino',
                'value': Cliente.objects.filter(sexo=2).count()
            },
            {
                'sexo': 'Femenino',
                'value': Cliente.objects.filter(sexo=1).exclude(cedula=1).count()
            }]

        context['json_info'] = json.dumps(json_info)

        return context

class ReporteEdadClientesRegistrados(TemplateView):
    template_name = "reportes/edad.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteEdadClientesRegistrados, self).get_context_data(**kwargs)

        actualizar_edad_clientes()

        rango_18_30 = 0
        rango_30_45 = 0
        rango_45_60 = 0
        rango_60_mas = 0

        clientes = Cliente.objects.all().exclude(cedula=1)

        for cliente in clientes:
            if cliente.edad >= 18 and cliente.edad < 30:
                rango_18_30 += 1
            elif cliente.edad >= 30 and cliente.edad < 45:
                rango_30_45 += 1
            elif cliente.edad >=45 and cliente.edad < 60:
                rango_45_60 += 1
            elif cliente.edad >= 60:
                rango_60_mas +=1

        info_json = [
            {
                'edad': 'entre 18 y 30 años',
                'value': rango_18_30
            },
            {
                'edad': 'entre 30 y 45 años',
                'value': rango_30_45
            },
            {
                'edad': 'entre 45 y 60 años',
                'value': rango_45_60
            },
            {
                'edad': 'igual o mayor a 60 años',
                'value': rango_60_mas
            },
        ]

        context['json_info'] = json.dumps(info_json)
        return context

class ReporteFacturas(TemplateView):
    template_name = "reportes/recaudos/facturas.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteFacturas, self).get_context_data(**kwargs)

        # Cambiar cuando se tenga un usuario propietario
        id_propietario = 1
        propietario = Propietario.objects.get(id_propietario=id_propietario)
        inmuebles_asociados = Inmueble.objects.filter(propietario=propietario)

        if kwargs['tipo'] == 'vencidas':
            facturas = PagosInmueble.objects.filter(
                pagada=False,
                fecha_limite_pago__lt = datetime.now().date(),
                inmueble__in=inmuebles_asociados
            ).order_by('fecha_limite_pago')

        elif kwargs['tipo'] == 'activas':
            facturas = PagosInmueble.objects.filter(
                pagada=False,
                inmueble__in=inmuebles_asociados,
            ).order_by('fecha_limite_pago')

        context['facturas'] = facturas
        context['campos'] = [
            'Número de factura',
            'Cliente',
            'Periodo facturado',
            'Valor pago',
            'Fecha límite de pago',
            'Inmueble asociado',
            'Tipo de transacción',
            'Acciones',
        ]

        return context

class SeguimientoPagosInmueble(TemplateView):
    template_name="reportes/recaudos/seguimiento.html"

    def get_context_data(self, **kwargs):
        context = super(SeguimientoPagosInmueble, self).get_context_data(**kwargs)

        # Cambiar cuando se tenga un usuario propietario
        id_propietario = 1
        propietario = Propietario.objects.get(id_propietario=id_propietario)
        inmuebles_asociados = Inmueble.objects.filter(propietario=propietario)

        inmuebles = Inmueble.objects.filter(propietario=propietario).order_by(
            'tipo_inmueble',
            'municipio__nombre',
            'barrio',
            'direccion'
        )

        context['inmuebles'] = inmuebles

        return context

    def post(self, request, *args, **kwargs):
        context = super(SeguimientoPagosInmueble, self).get_context_data(**kwargs)

        codigo_inmueble = request.POST['inmueble']

        # Cambiar cuando se tenga un usuario propietario
        id_propietario = 1
        propietario = Propietario.objects.get(id_propietario=id_propietario)
        inmuebles = Inmueble.objects.filter(propietario=propietario).order_by(
            'tipo_inmueble',
            'municipio__nombre',
            'barrio',
            'direccion'
        )

        context['inmuebles'] = inmuebles

        if codigo_inmueble == 0:
            messages.add_message(self.request, messages.ERROR, 'Debe seleccionar un inmueble')

        else:
            # Cambiar cuando se tenga un usuario propietario
            id_propietario = 1
            propietario = Propietario.objects.get(id_propietario=id_propietario)
            inmuebles_asociados = Inmueble.objects.filter(propietario=propietario)

            numero_facturas = 12
            if request.POST['numero-facturas']:
                numero_facturas = int(request.POST['numero-facturas'])

            facturas = PagosInmueble.objects.all().order_by('-fecha_limite_pago')[:numero_facturas]
            context['facturas'] = facturas

            context['campos'] = [
                'Número de factura',
                'Cliente',
                'Periodo facturado',
                'Valor a pagar',
                'Concepto',
                'Fecha de generación factura',
                'Fecha límite de pago',
                'Fecha de pago',
                'Días de mora',
            ]

            context['inmueble'] = Inmueble.objects.get(codigo=codigo_inmueble)

        return render(request, self.template_name, context)

class EstadoPagos(TemplateView):
    template_name = "reportes/recaudos/estado_pagos.html"

    def post(self, request, *args, **kwargs):
        context = super(EstadoPagos, self).get_context_data(**kwargs)

        periodo_facturado = request.POST['periodo_facturado']
        periodo = periodo_facturado.split(" - ")
        print(periodo)

        fecha_inicio = periodo[0]
        fecha_fin = periodo[1]

        formato = "%m/%d/%Y"
        nuevo_formato = "%Y-%m-%d"

        fecha_inicio_formato = datetime.strptime(fecha_inicio, formato).date()
        fecha_fin_formato = datetime.strptime(fecha_fin, formato).date()

        if fecha_inicio_formato == fecha_fin_formato and fecha_inicio_formato == datetime.now().date():
            fecha_inicio_formato = fecha_fin_formato - timedelta(days=30)

        facturas = PagosInmueble.objects.filter(
            fecha_emision_factura__gte=fecha_inicio_formato,
            fecha_emision_factura__lte=fecha_fin_formato+timedelta(days=1),
        ).order_by('fecha_emision_factura')

        numero_pagadas = facturas.filter(pagada=True).count()
        numero_activas = facturas.filter(pagada=False, fecha_limite_pago__gte=datetime.now()).count()
        numero_vencidas = facturas.filter(pagada=False, fecha_limite_pago__lte=datetime.now()).count()

        json_info = [
            {
                'tipo_factura': 'Facturas pagadas',
                'value': numero_pagadas
            },
            {
                'tipo_factura': 'Facturas no pagadas no vencidas',
                'value': numero_activas
            },
            {
                'tipo_factura': 'Facturas vencidas',
                'value': numero_vencidas
            }
        ]

        context['json_info'] = json.dumps(json_info)
        context['periodo_json'] = json.dumps([{'periodo': periodo_facturado}])
        context['cantidad_facturas'] = len(facturas)
        context['periodo'] = periodo_facturado
        context['fecha_inicio'] = fecha_inicio_formato
        context['fecha_fin'] = fecha_fin_formato

        return render(request, self.template_name, context)

class ConsultarCalendarioCitas(TemplateView):
    template_name = "reportes/citas/calendario_citas.html"

class ReporteInmueblesPorTipo(TemplateView):
    template_name = "reportes/tipo_inmuebles.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteInmueblesPorTipo, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name='propietario').exists():
            propietario = Propietario.objects.get(usuario=self.request.user)

            json_info = [
                {
                    'tipo inmueble': 'Casas',
                    'value': Inmueble.objects.filter(
                        tipo_inmueble=1,
                        estado=True,
                        propietario=propietario
                    ).count()
                },
                {
                    'tipo inmueble': 'Apartamentos',
                    'value': Inmueble.objects.filter(
                        tipo_inmueble=2,
                        estado=True,
                        propietario=propietario
                    ).count()
                },
                {
                    'tipo inmueble': 'Locales',
                    'value': Inmueble.objects.filter(
                        tipo_inmueble=3,
                        estado=True,
                        propietario=propietario
                    ).count()
                }
            ]

            context['json_info'] = json.dumps(json_info)

            return context

        else:
            raise PermissionDenied("No tiene permisos para ver esta página")

class ReporteInmueblesDisponiblesOcupados(TemplateView):
    template_name = "reportes/inmuebles_dispo_ocupados.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteInmueblesDisponiblesOcupados, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name='propietario').exists():
            propietario = Propietario.objects.get(usuario=self.request.user)

            json_info = [
                {
                    'estado': 'Disponible',
                    'value': Inmueble.objects.filter(
                        estado_operacional=1,
                        estado=True,
                        propietario=propietario
                    ).count()
                },
                {
                    'estado': 'Ocupado',
                    'value': Inmueble.objects.filter(
                        estado_operacional=2,
                        estado=True,
                        propietario=propietario
                    ).count()
                },
                {
                    'estado': 'En remodelación',
                    'value': Inmueble.objects.filter(
                        estado_operacional=3,
                        estado=True,
                        propietario=propietario
                    ).count()
                },
            ]

            context['json_info'] = json.dumps(json_info)

            return context

        else:
            raise PermissionDenied("No tiene permisos para ver esta página")
