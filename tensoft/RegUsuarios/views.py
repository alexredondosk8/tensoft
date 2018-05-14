from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from datetime import datetime
from .models import Usuario
from .forms import *
# from .utils import *

class ClienteUsuario(TemplateView):
    template_name = "RegUsuarios/cliente_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClienteUsuario, self).get_context_data(**kwargs)
        context['form'] = FormRegistroCliente

        return context

    def post(self, request, *args, **kwargs):
        context = super(ClienteUsuario, self).get_context_data(**kwargs)
        print(request.POST)

        form_cliente = FormRegistroCliente(request.POST)

        if form_cliente.is_valid():
            datos = form_cliente.cleaned_data
            nombre = datos['nombre']
            apellidos = datos['apellidos']
            correo = datos['correo']
            telefono = datos['telefono']
            celular = datos['celular']

# se definen los datos

        cliente_registrado = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            celular=celular
        )

        cliente_registrado.save()
        request.session['correo'] = correo

        return HttpResponseRedirect('/cuenta/registrar/usuario')
