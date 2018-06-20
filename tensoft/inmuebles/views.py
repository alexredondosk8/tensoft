from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.contrib import messages
import simplejson as json
from datetime import datetime, timedelta
from .models import *
from propietarios.models import *
from RegUsuarios.models import *
from pagos.models import *
from .forms import *
from .utils import *
from reportes.views import *

# Create your views here.
class InmueblesCreateView(CreateView):
    #get_success_url = "/inmuebles/lista/?estado=1"
    model = Inmueble
    fields = [
        'tipo_inmueble',
        'tipo_transaccion',
        'tipo_moneda',
        'valor',
        'area',
        'numero_baños',
        'numero_habitaciones',
        'parqueadero',
        'tipo_parqueadero',
        'parqueadero_visitantes',
        'barrio',
        'direccion',
        'municipio',
        'estrato',
        'descripcion',
        'propietario'
    ]

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(InmueblesCreateView, self).get_form(form_class)

        ########### CAMBIAR CUANDO HAYA USUARIO #############
        #propietario = Propietario.objects.get(pk=1)
        propietario = Propietario.objects.get(usuario=self.request.user)

        form.fields['propietario'].initial = propietario.id_propietario
        form.fields['propietario'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super(InmueblesCreateView, self).get_context_data(**kwargs)
        context['municipios'] = get_municipios_dpto()
        return context

    def form_valid(self, form):
        inmueble_instancia = form.instance
        self.object = form.save()
        codigo = self.object.codigo
        self.success_url = "/inmuebles/registrar/" + str(codigo) + "/fotos/"
        return super().form_valid(form)

class AgregarFotosInmueble(TemplateView):
    template_name = "inmuebles/registrar_fotos_inmueble.html"

    def get_context_data(self, **kwargs):
        context = super(AgregarFotosInmueble, self).get_context_data(**kwargs)

        form = FormRegistrarFoto()
        context['form'] = form

        context['inmueble'] = Inmueble.objects.get(codigo=kwargs['id_inmueble'])

        return context

    def post(self, request, *args, **kwargs):
        context = super(AgregarFotosInmueble, self).get_context_data(**kwargs)

        inmueble = Inmueble.objects.get(codigo=kwargs['id_inmueble'])
        context['inmueble'] = inmueble

        form = FormRegistrarFoto(request.POST, request.FILES)
        context['form'] = form

        if form.is_valid():
            imagenes = request.FILES.getlist('imagen')

            for imagen in imagenes:
                inmueble_imagen = FotosInmueble(codigo=inmueble, imagen=imagen)
                inmueble_imagen.save()

            messages.add_message(request, messages.SUCCESS, 'Se añadieron las imágenes del inmuebles'
                ' exitosamente')

        return HttpResponseRedirect("/inmuebles/" + str(inmueble.codigo) + "/")

class ListarInmuebles(ListView):
    model = Inmueble
    template_name = "inmuebles/lista_inmuebles.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListarInmuebles, self).get_context_data(**kwargs)
        lista_inmuebles = []

        if 'estado' in self.request.GET:
            estado = self.request.GET['estado']
            lista_inmuebles = get_lista_inmuebles(self.request.user, estado)
            context['var_pdf'] = "estado_operacional"
            context['id'] = estado

            if estado == '1':
                context['tipo_lista'] = "Inmuebles disponibles"
            elif estado == '2':
                context['tipo_lista'] = "Inmuebles ocupados"
            elif estado == '3':
                context['tipo_lista'] = "Inmuebles no disponibles"

        elif 'tipo' in self.request.GET:
            ########### CAMBIAR CUANDO HAYA USUARIO ###########
            tipo = self.request.GET['tipo']
            context['var_pdf'] = "tipo_inmueble"
            context['id'] = tipo
            if self.request.user.groups.filter(name='propietario').exists():
                propietario = Propietario.objects.get(usuario=self.request.user)
                lista_inmuebles = get_lista_inmuebles_por_tipo(tipo, propietario)

            elif self.request.user.groups.filter(name='usuario-inmobiliaria').exists():
                lista_inmuebles = get_lista_inmuebles_por_tipo(tipo)

            if tipo == '1':
                context['tipo_lista'] = "Casas"
            elif tipo == '2':
                context['tipo_lista'] = "Apartamentos"
            elif tipo == '3':
                context['tipo_lista'] = "Locales"
            else:
                print(tipo)

        paginator = Paginator(lista_inmuebles, self.paginate_by)

        context['campos'] = ['Código', 'Fecha de registro', 'Área', 'Barrio', 'Acción']
        context['lista_inmuebles'] = lista_inmuebles

        return context

class ListarInmueblesActivos(ListView):
    model = Inmueble
    template_name = "inmuebles/lista_inmuebles.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListarInmueblesActivos, self).get_context_data(**kwargs)

        lista_inmuebles = get_lista_inmuebles(self.request.user)
        paginator = Paginator(lista_inmuebles, self.paginate_by)

        context['tipo_lista'] = 'Inmuebles registrados'
        context['campos'] = ['Código', 'Fecha de registro', 'Área', 'Barrio', 'Estado', 'Acción']

        context['lista_inmuebles'] = lista_inmuebles

        return context

class DetallesInmueble(DetailView):

    model = Inmueble

    def get_context_data(self, **kwargs):


        context = super(DetallesInmueble, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name='propietario').exists():

            context['propietario'] = "true"

            imagenes = FotosInmueble.objects.filter(codigo=kwargs['object'].codigo)
            context['imagenes'] = imagenes

        return context

    def post(self, request, *args, **kwargs):
        estado_operacional = request.POST['estado_operacional']

        inmueble = Inmueble.objects.get(codigo=kwargs['pk'])

        if inmueble.estado_operacional != estado_operacional:
            inmueble.estado_operacional = estado_operacional
            inmueble.save()

        messages.add_message(self.request, messages.SUCCESS,
                             'Se actualizó la información del estado exitosamente')

        return render(request, self.template_name)
        #return HttpResponseRedirect("")

class ActualizarInmueble(UpdateView):
    model = Inmueble
    fields = [
        'tipo_inmueble',
        'tipo_transaccion',
        'tipo_moneda',
        'valor',
        'area',
        'numero_baños',
        'numero_habitaciones',
        'parqueadero',
        'tipo_parqueadero',
        'parqueadero_visitantes',
        'barrio',
        'direccion',
        'municipio',
        'estrato',
        'descripcion'
    ]
    template_name = "inmuebles/actualizar_inmueble.html"

    def get_context_data(self, **kwargs):
        context = super(ActualizarInmueble, self).get_context_data(**kwargs)
        context['municipios'] = get_municipios_dpto()
        context['municipio_inmueble'] = get_municipio_inmueble(Inmueble.objects.get(codigo=context['inmueble'].codigo))
        print(context['municipio_inmueble'].id_municipio)
        return context

    def form_valid(self, form):
        print(self.request.POST)
        """form.instance.created_by = self.request.user"""
        messages.add_message(self.request, messages.SUCCESS, 'Se actualizó la información del inmueble'
            ' exitosamente')
        return super().form_valid(form)

class InmueblesMapa(TemplateView):
    template_name = "inmuebles/mapa.html"

    def get_context_data(self, **kwargs):
        context = super(InmueblesMapa, self).get_context_data(**kwargs)

        inmuebles = Inmueble.objects.all()
        info_mapa = []
        for inmueble in inmuebles:
            info_inmueble = {
                'direccion': inmueble.direccion,
                'ciudad': inmueble.municipio.nombre,
                'pais': 'Colombia',
                'url': '/inmuebles/' + str(inmueble.codigo) + "/",
                'tipo_inmueble': inmueble.get_tipo_inmueble(),
                'barrio': inmueble.barrio,
            }
            info_mapa.append(info_inmueble)

        context['inmuebles'] = json.dumps(info_mapa)

        return context

class GenerarFacturaPago(TemplateView):
    template_name = "pagos/generar_factura.html"

    def get_context_data(self, **kwargs):
        context = super(GenerarFacturaPago, self).get_context_data(**kwargs)
        inmueble = Inmueble.objects.get(codigo=kwargs['id_inmueble'])
        context['inmueble'] = inmueble

        return context

    def post(self, request, *args, **kwargs):
        context = super(GenerarFacturaPago, self).get_context_data(**kwargs)
        inmueble = Inmueble.objects.get(codigo=kwargs['id_inmueble'])
        context['inmueble'] = inmueble

        periodo_facturado = request.POST['periodo_facturado']
        periodo = periodo_facturado.split(" - ")
        print(periodo)

        fecha_inicio = periodo[0]
        fecha_fin = periodo[1]

        formato = "%m/%d/%Y"
        nuevo_formato = "%Y-%m-%d"

        fecha_inicio_formato = datetime.strptime(fecha_inicio, formato).date()
        fecha_fin_formato = datetime.strptime(fecha_fin, formato).date()

        if fecha_inicio_formato < fecha_fin_formato:

            factura = PagosInmueble(
                periodo_inicio_factura = fecha_inicio_formato,
                periodo_final_factura = fecha_fin_formato,
                fecha_limite_pago = datetime.now()+timedelta(days=10),
                valor_pago = inmueble.valor,
                tipo_moneda = inmueble.tipo_moneda,
                tipo_pago = inmueble.tipo_transaccion,
                # CAMBIAR CUANDO SE TENGAN USUARIOS ENLAZADOS
                usuario = Usuario.objects.get(cedula='25353525'),
                inmueble = inmueble,
            )

            factura.save()

            messages.add_message(request, messages.SUCCESS, 'Se emitió la factura exitosamente')

            return render(request, self.template_name, context)

        else:
            messages.add_message(request, messages.ERROR, 'La fecha de finalización debe ser mayor a '+
                'la fecha de inicio del periodo')
            return render(request, self.template_name, context)

class BuscarInmuebles(TemplateView):
    template_name = "inmuebles/buscar_inmuebles.html"

    def post(self, request, *args, **kwargs):
        context = super(BuscarInmuebles, self).get_context_data(**kwargs)
        print(request.POST)
        if 'buscar_x_codigo' in request.POST:
            codigo = request.POST['codigo']

            if codigo:
                inmueble = Inmueble.objects.get(codigo=codigo)
                if inmueble:
                    context['inmueble'] = inmueble
                else:
                    context['no_existe'] = "No se encontró ningún inmueble con el código proporcionado"

            else:
                context['codigo_vacio'] = "Debe proporcionar un código para buscar el inmueble"

        return render(request, self.template_name, context)
