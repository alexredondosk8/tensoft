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
           request.session['identificacion'] = identificacion
           return render(self.request, "app/index.html")

       else:
           context['form'] = form_propietario
           return render(request, self.template_name, context)