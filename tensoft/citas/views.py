from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from .models import *
from .utils import *
from RegUsuarios.models import *
from django.contrib import messages
# Create your views here.
class CitasCreateView(CreateView):
    model = Citas
    fields = [
        'id_cita',
        'codigo',
        'fecha_cita',
        'hora_cita',
        'hora_fin_cita',
        'cedula',
        'comentarios']

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CitasCreateView, self).get_form(form_class)
        form.fields['codigo'].initial = self.kwargs['id']
        form.fields['codigo'].disabled = True
        #usuario = Usuario.objects.get(usuario=self.request.user)
        #form.fields['usuario']=usuario
        form.fields['fecha_cita'].initial=datetime.now()

        print(self)
        return form

class ListarCitas(ListView):
    model = Citas
    template_name = "citas/lista_citas.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListarCitas, self).get_context_data(**kwargs)

        estado = self.request.GET['estado']

        lista_citas = get_lista_citas(self.request.user, estado)
        paginator = Paginator(lista_citas, self.paginate_by)

        context['tipo_lista'] = estado
        context['campos'] = ['Id Cita', 'Inmueble', 'Fecha de cita', 'Acción']

        context['lista_citas'] = lista_citas

        return context

class DetallesCita(DetailView):

    model = Citas

class ActualizarCita(UpdateView):
    model = Citas
    fields = [
        'fecha_cita',
        'hora_cita',
        'hora_fin_cita']

    template_name = "citas/actualizar_cita.html"

    def get_context_data(self, **kwargs):
        context = super(ActualizarCita, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        print(self.request.POST)
        """form.instance.created_by = self.request.user"""
        messages.add_message(self.request, messages.SUCCESS, 'Se actualizó la información de la cita'
            ' exitosamente')
        return super().form_valid(form)
