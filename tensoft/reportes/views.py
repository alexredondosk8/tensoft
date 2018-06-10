from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import simplejson as json
from django.template import Context
from django.template.loader import get_template
from weasyprint import HTML, CSS
from datetime import datetime
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

class ReporteListaInmuebles(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super(ReporteListaInmuebles, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        formato = kwargs['formato']
        estado = int(kwargs['id'])

        context['inmuebles'] = Inmueble.objects.filter(estado=estado).order_by('-fecha_registro')
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

        print(info_json)

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
                'Fecha de generación factura',
                'Fecha límite de pago',
                'Fecha de pago',
                'Días de mora',
            ]

            context['inmueble'] = Inmueble.objects.get(codigo=codigo_inmueble)

        return render(request, self.template_name, context)
