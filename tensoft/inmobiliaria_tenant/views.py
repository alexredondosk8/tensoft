from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import Cliente, Inmobiliaria

# Create your views here.
class Inicio(TemplateView):
    template_name = 'app/index.html'

class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', "apellidos", "cedula", "correo"]
    success_url = "/cuenta/registrar/usuario"

    def form_valid(self, form):
        cliente_registrado = form.instance
        self.request.session['cedula'] = self.request.POST['cedula']
        self.object = form.save()

        return super(ClienteCreateView, self).form_valid(form)

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

        return render(request, "/cuenta/login/", context)

class Login(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        registro_exitoso = self.request.session.get('nuevo-registro')
        if registro_exitoso:
            context['registro'] = registro_exitoso
            del self.request.session['nuevo-registro']
        """usuario_actual = self.request.user
        context['usuario'] = usuario_actual.username"""
        return context

    def post(self, request, *args, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print (user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            context['no_usuario'] = 'Usuario o contraseña inválidos'
        return render(request, 'registration/login.html', context)

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
                    schema_name = nombre_inmobiliaria.lower()
                )
                inmobiliaria.save()
        else:
            context['vacio'] = "El nombre de la inmobiliaria debe contener un valor válido"
            context['cliente'] = Cliente.objects.get(usuario=self.request.user)
            return render(request, self.template_name, context)

        return HttpResponseRedirect('/inmobiliarias/pendientes/')

class InmobiliariasPendientes(TemplateView):
    template_name = "app/plain_page.html"
