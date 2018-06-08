from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import simplejson as json
from django.template import Context
from django.template.loader import get_template
from weasyprint import HTML, CSS
from inmobiliaria_tenant.models import *
from inmuebles.models import *
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
