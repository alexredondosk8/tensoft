from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from datetime import datetime
from .forms import *
from .utils import *
from .models import *

# Create your views here.
class PropietarioCreateView(TemplateView):
   '''
    model = Propietario
    fields = [
        'identificacion',
        'nombres',
        'apellidos',
        'direccion',
        'telefono',
        'email']
   '''
   template_name = "propietarios/propietarios_form.html"

   def get_context_data(self, **kwargs):
       context = super(PropietarioCreateView, self).get_context_data(**kwargs)
       context['form'] = FormRegistroPropietario

       return context

   def post(self, request, *args, **kwargs):
       context = super(PropietarioCreateView, self).get_context_data(**kwargs)

       form_propietario = FormRegistroPropietario(request.POST)

       if form_propietario.is_valid():
           datos = form_propietario.cleaned_data
           nombres = datos['nombres']
           apellidos = datos['apellidos']
           identificacion = datos['identificacion']
           email = datos['email']
           direccion = datos['direccion']
           telefono = datos['telefono']
           propietario_registrado = Propietario(
               nombres=nombres,
               apellidos=apellidos,
               identificacion=identificacion,
               email=email,
               direccion=direccion,
               telefono=telefono
           )

           propietario_registrado.save()

           # try:
           #     grupo = Group.objects.get(name='propietario-inmobiliaria')
           #     grupo.user_set.add(nuevo_usuario)
           # except:
           #     grupo = Group()
           #     grupo.name = 'propietario-inmobiliaria'
           #     grupo.save()
           #     grupo.user_set.add(nuevo_usuario)

           request.session['identificacion'] = identificacion
           return render(self.request, "app/index.html")

       else:
           context['form'] = form_propietario
           return render(request, self.template_name, context)


class ListarPropietarios(ListView):
    model = Propietario
    template_name = "propietarios/lista_propietarios.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListarPropietarios, self).get_context_data(**kwargs)
        print(context)

        #estado = self.request.GET['estado']

        #lista_propietarios = get_lista_propietarios(self.request.user)
        lista_propietarios = Propietario.objects.all()
        print (lista_propietarios[0].nombres)
        paginator = Paginator(lista_propietarios, self.paginate_by)

        #context['tipo_lista'] = estado
        context['campos'] = ['Identificacion', 'Nombres', 'Apellidos', 'Direccion', 'Email', 'Telefono']

        context['lista_propietarios'] = lista_propietarios

        return context


class ActualizarPropietario(UpdateView):
    model = Propietario
    fields = [
        'nombres',
        'apellidos',
        'identificacion',
        'email',
        'direccion',
        'telefono'
    ]
    template_name = "propietarios/actualizar_propietario.html"

    def get_context_data(self, **kwargs):
        context = super(ActualizarPropietario, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        #context = super(ActualizarPropietario, self).get_context_data(**kwargs)
        """form.instance.created_by = self.request.user"""
        #messages.add_message(self.request, messages.SUCCESS, 'Se actualizó la información del Propietario exitosamente')
        return super().form_valid(form)
        #return HttpResponseRedirect("propietarios/lista_propietarios.html")

        #return render(self.request, self.template_name, None)
    #
    # template_name = "inmobiliaria_tenant/actualizar_cliente.html"
    #
    # # form_class = FormUpdateCliente

    # def get_context_data(self, **kwargs):
    #     context = super(ClienteUpdateView, self).get_context_data(**kwargs)
    #
    #     cliente = Cliente.objects.get(usuario=self.request.user)
    #     context['cliente'] = cliente
    #
    #     form = FormUpdateCliente(instance=cliente)
    #     context['form'] = form
    #
    #     return context

    # def post(self, request, *args, **kwargs):
    #     context = super(ActualizarPropietario, self).get_context_data(**kwargs)
    #     form = FormUpdatePropietario(request.POST)
    #     context['form'] = form
    #
    #     if form.is_valid():
    #         identificacion = form.cleaned_data['identificacion']
    #         nombre = form.cleaned_data['nombre']
    #         apellidos = form.cleaned_data['apellidos']
    #         direccion = form.cleaned_data['direccion']
    #         telefono = form.cleaned_data['telefono']
    #         email = form.cleaned_data['email']
    #
    #         propietario = Propietario.objects.get(usuario=self.request.user)
    #         context['propietario'] = propietario
    #
    #         propietario.identificacion = identificacion
    #         propietario.nombre = nombre
    #         propietario.apellidos = apellidos
    #         propietario.direccion= direccion
    #         propietario.telefono = telefono
    #         propietario.email = email
    #
    #         propietario.save()
    #
    #         context['success'] = "Los datos han sido actualizados correctamente"
    #
    #     return render(request, self.template_name, context)