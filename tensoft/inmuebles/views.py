from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.contrib import messages
from .models import *
from .forms import *
from .utils import *

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
        'descripcion']

    def get_context_data(self, **kwargs):
        context = super(InmueblesCreateView, self).get_context_data(**kwargs)
        context['municipios'] = get_municipios_dpto()
        return context

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

        estado = self.request.GET['estado']

        lista_inmuebles = get_lista_inmuebles(self.request.user, estado)
        paginator = Paginator(lista_inmuebles, self.paginate_by)

        context['tipo_lista'] = estado
        context['campos'] = ['Código', 'Fecha de registro', 'Área', 'Barrio', 'Acción']

        context['lista_inmuebles'] = lista_inmuebles

        return context

class DetallesInmueble(DetailView):

    model = Inmueble

    def get_context_data(self, **kwargs):
        context = super(DetallesInmueble, self).get_context_data(**kwargs)

        print(self.request)

        imagenes = FotosInmueble.objects.filter(codigo=kwargs['object'].codigo)
        context['imagenes'] = imagenes

        return context
