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

class Inicio(TemplateView):
    template_name = 'app/index.html'

class UsuarioCreateView(TemplateView):
    template_name = "RegUsuarios/cliente_form.html"

    def get_context_data(self, **kwargs):
        context = super(UsuarioCreateView, self).get_context_data(**kwargs)
        context['form'] = FormRegistroCliente

        return context

    def post(self, request, *args, **kwargs):
        context = super(UsuarioCreateView, self).get_context_data(**kwargs)
        print(request.POST)

        form_cliente = FormRegistroCliente(request.POST)

        if form_cliente.is_valid():
            datos = form_cliente.cleaned_data
            nombre = datos['nombre']
            apellidos = datos['apellidos']
            cedula = datos['cedula']
            correo = datos['correo']
            telefono = datos['telefono']
            celular = datos['celular']

            # VALIDA QUE EL CORREO NO ESTÉ REGISTRADO EN LA BD
            try:
                usuario = User.objects.get(username=correo)
                context['form'] = form_cliente
                context['existe'] = "Ya existe una cuenta vinculada con el correo" + correo + "."
                return render(request, self.template_name, context)

            except:
                # se definen los datos
                cliente_registrado = Usuario(
                    nombre=nombre,
                    apellidos=apellidos,
                    cedula=cedula,
                    correo=correo,
                    telefono=telefono,
                    celular=celular
                )
                cliente_registrado.save()
                request.session['correo'] = correo

                return HttpResponseRedirect('/cuenta/registrar/usuario')
        else:
            context['form'] = form_cliente
            return render(request, self.template_name, context)

class UsuarioClienteCreateView(TemplateView):
    model = User
    success_url = "/cuenta/login"
    template_name = "RegUsuarios/user_form.html"

    def get_context_data(self, **kwargs):
        context = super(UsuarioClienteCreateView, self).get_context_data(**kwargs)

        if self.request.session.get('correo'):
            cliente = Usuario.objects.get(cedula=self.request.session.get('correo'))
            context['cliente'] = cliente

        else:
            raise PermissionDenied

        return context

    def post(self, request, *args, **kwargs):
        context = super(UsuarioClienteCreateView, self).get_context_data(**kwargs)
        if request.POST['password'] and request.POST['password2']:
            if request.POST['password'] == request.POST['password2']:
                password = request.POST['password']
                correo = cliente.correo
                nuevo_usuario = User.objects.create_user(username=correo, password=password)
                nuevo_usuario.save()
                cliente.usuario = nuevo_usuario
                cliente.save()

                try:
                    grupo = Group.objects.get(name='usuario-inmobiliaria')
                    grupo.user_set.add(nuevo_usuario)
                except:
                    grupo = Group()
                    grupo.name = 'usuario-inmobiliaria'
                    grupo.save()
                    grupo.user_set.add(nuevo_usuario)

                del request.session['correo']
                request.session['nuevo-registro'] = "Usted se ha registrado exitosamente. Por favor inicie sesión para continuar"

            else:
                cliente = Cliente.objects.get(cedula=self.request.session.get('cedula'))
                context['cliente'] = cliente
                context['no_match'] = "Las contraseñas no coinciden"
                return render(request, self.template_name, context)

            return redirect("/cuenta/login/", request=request)

class Login(TemplateView):
    template_name = "login.html"
    
class CuentaUsuario(TemplateView):
    template_name = "RegUsuarios/cuenta_cliente.html"
