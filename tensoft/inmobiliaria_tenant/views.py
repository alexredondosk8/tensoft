from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView, CreateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from datetime import datetime
from .models import Cliente, Inmobiliaria, Domain
from .forms import *
from .utils import *

# Create your views here.
class Inicio(TemplateView):
    template_name = 'app/index.html'

class ClienteCreateView(TemplateView):
    template_name = "inmobiliaria_tenant/cliente_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context['form'] = FormRegistroCliente

        return context

    def post(self, request, *args, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        print(request.POST)

        form_cliente = FormRegistroCliente(request.POST)

        if form_cliente.is_valid():
            datos = form_cliente.cleaned_data
            nombre = datos['nombre']
            apellidos = datos['apellidos']
            cedula = datos['cedula']
            correo = datos['correo']

            # VALIDA QUE EL CORREO NO ESTÉ REGISTRADO EN LA BD
            try:
                usuario = User.objects.get(username=correo)
                context['form'] = form_cliente
                context['existe'] = "Ya existe una cuenta vinculada con el correo " + correo + "."
                return render(request, self.template_name, context)

            except:
                cliente_registrado = Cliente(
                    nombre=nombre,
                    apellidos=apellidos,
                    cedula=cedula,
                    correo=correo
                )

                cliente_registrado.save()
                request.session['cedula'] = cedula

                return HttpResponseRedirect('/cuenta/registrar/usuario')
        else:
            context['form'] = form_cliente
            return render(request, self.template_name, context)

class UsuarioClienteCreateView(TemplateView):
    model = User
    success_url = "/cuenta/login"
    template_name = "inmobiliaria_tenant/user_form.html"

    def get_context_data(self, **kwargs):
        context = super(UsuarioClienteCreateView, self).get_context_data(**kwargs)
        #del self.request.session['cedula']
        if self.request.session.get('cedula'):
            cliente = Cliente.objects.get(cedula=self.request.session.get('cedula'))
            context['cliente'] = cliente
            #del self.request.session['cedula']

        else:
            raise PermissionDenied

        return context

    def post(self, request, *args, **kwargs):
        context = super(UsuarioClienteCreateView, self).get_context_data(**kwargs)
        if request.POST['password'] and request.POST['password2']:
            if request.POST['password'] == request.POST['password2']:
                password = request.POST['password']
                cliente = Cliente.objects.get(cedula=request.session['cedula'])
                correo = cliente.correo
                nuevo_usuario = User.objects.create_user(username=correo, password=password)
                nuevo_usuario.save()
                cliente.usuario = nuevo_usuario
                cliente.save()

                try:
                    grupo = Group.objects.get(name='cliente-inmobiliaria')
                    grupo.user_set.add(nuevo_usuario)
                except:
                    grupo = Group()
                    grupo.name = 'cliente-inmobiliaria'
                    grupo.save()
                    grupo.user_set.add(nuevo_usuario)

                del request.session['cedula']
                request.session['nuevo-registro'] = "Usted se ha registrado exitosamente. Por favor inicie sesión para continuar"

            else:
                cliente = Cliente.objects.get(cedula=self.request.session.get('cedula'))
                context['cliente'] = cliente
                context['no_match'] = "Las contraseñas no coinciden"
                return render(request, self.template_name, context)
        else:
            context['vacio'] = 'Los campos de contraseña deben tener valores válidos'
            cliente = Cliente.objects.get(cedula=self.request.session.get('cedula'))
            context['cliente'] = cliente
            return render(request, self.template_name, context)

        return redirect("/cuenta/login/", request=request)

class Login(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        print(kwargs)
        registro_exitoso = self.request.session.get('nuevo-registro')
        if registro_exitoso:
            context['registro'] = registro_exitoso
            del self.request.session['nuevo-registro']
        else:
            print("nada en el session para mostrar")
        return context

    def post(self, request, *args, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print (context)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            context['no_usuario'] = 'Usuario o contraseña inválidos'
        return render(request, self.template_name, context)

class RegistrarInmobiliaria(TemplateView):
    model = Inmobiliaria
    fields = ['nombre', 'representante']
    template_name = "inmobiliaria_tenant/inmobiliaria_form.html"

    def get_context_data(self, **kwargs):
        context = super(RegistrarInmobiliaria, self).get_context_data(**kwargs)
        cliente = Cliente.objects.get(usuario=self.request.user)
        context['cliente'] = cliente
        self.request.session['cliente_cedula'] = cliente.cedula

        return context

    def post(self, request, *args, **kwargs):
        context = super(RegistrarInmobiliaria, self).get_context_data(**kwargs)
        nombre_inmobiliaria = request.POST['nombre']

        if nombre_inmobiliaria:
            if " " in nombre_inmobiliaria:
                context['espacios'] = "El nombre de la inmobiliaria no puede contener espacios"
                context['cliente'] = Cliente.objects.get(usuario=request.user)
                return render(request, self.template_name, context)
            else:
                inmobiliaria = Inmobiliaria(
                    nombre = nombre_inmobiliaria,
                    representante = Cliente.objects.get(usuario=request.user),
                    schema_name = procesar_schema_name(nombre_inmobiliaria).lower()
                )
                inmobiliaria.save()
        else:
            context['vacio'] = "El nombre de la inmobiliaria debe contener un valor válido"
            context['cliente'] = Cliente.objects.get(usuario=self.request.user)
            return render(request, self.template_name, context)

        return HttpResponseRedirect('/inmobiliarias/pendientes-alta/')

class InmobiliariasPendientesAprobacionAlta(ListView):
    model = Inmobiliaria
    template_name = "inmobiliaria_tenant/lista_inmobiliarias.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(InmobiliariasPendientesAprobacionAlta, self).get_context_data(**kwargs)

        if self.request.user.is_superuser or self.request.user.groups.filter(name='cliente-inmobiliaria').exists():
            context = super(InmobiliariasPendientesAprobacionAlta, self).get_context_data(**kwargs)
            lista_inmobiliarias = lista_inmobiliarias_pendientes(self.request.user)
            paginator = Paginator(lista_inmobiliarias, self.paginate_by)

            context['tipo_lista'] = 'Para dar Alta'

            if self.request.user.is_superuser:
                context['campos'] = ['Nombre', 'Fecha de registro', 'Fecha de aprobación',
                                'Estado', 'Representante', 'Acción solicitada']
            elif self.request.user.groups.filter(name='cliente-inmobiliaria').exists():
                context['campos'] = ['Nombre', 'Fecha de registro', 'Fecha de aprobación',
                                'Estado']
            context['lista'] = lista_inmobiliarias
        else:
            raise PermissionDenied

        return context

class DetallesInmobiliaria(TemplateView):
    template_name = "inmobiliaria_tenant/detalles_inmobiliaria.html"

    def get_context_data(self, **kwargs):
        context = super(DetallesInmobiliaria, self).get_context_data(**kwargs)

        inmobiliaria = Inmobiliaria.objects.get(id=kwargs['id'])
        context['inmobiliaria'] = inmobiliaria

        if 'success' in self.request.session:
            context['success'] = self.request.session['success']
            del self.request.session['success']

        return context

    def post(self, request, *args, **kwargs):
        context = super(DetallesInmobiliaria, self).get_context_data(**kwargs)

        inmobiliaria = Inmobiliaria.objects.get(id=kwargs['id'])
        context['inmobiliaria'] = inmobiliaria

        if 'aprobar_alta' in request.POST:
            inmobiliaria.estado=True
            inmobiliaria.create_schema()
            dominio_inmobiliaria = Domain(
                domain=inmobiliaria.schema_name+'.localhost',
                is_primary=True,
                tenant=inmobiliaria
            )
            dominio_inmobiliaria.save()

            request.session['success'] = "Se ha aprobado la inmobiliaria exitosamente"

        elif 'rechazar_alta' in request.POST:
            request.session['success'] = "Se ha rechazado la inmobiliaria exitosamente"

        inmobiliaria.fecha_revision=datetime.now()
        inmobiliaria.save()

        return render(request, self.template_name, context)
