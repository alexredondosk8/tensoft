from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.core.exceptions import PermissionDenied
from .models import Cliente

# Create your views here.
class Inicio(TemplateView):
    template_name = 'app/index.html'

class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', "apellidos", "cedula", "correo"]
    success_url = "/cuenta/registrar/usuario"

    def form_valid(self, form):
        cliente_registrado = form.instance
        self.request.session['cliente-registrado'] = self.request.POST['correo']
        print(self.request.session.get('cliente-registrado'), 'este es el correo')
        self.object = form.save()

        return super(ClienteCreateView, self).form_valid(form)

class UsuarioClienteCreateView(TemplateView):
    model = User
    success_url = "/cuenta/login"
    template_name = "inmobiliaria_tenant/user_form.html"

    def get_context_data(self, **kwargs):
        context = super(UsuarioClienteCreateView, self).get_context_data(**kwargs)
        if self.request.session.get('cliente-registrado'):
            context['cliente'] = self.request.session.get('cliente-registrado')
            del self.request.session['cliente-registrado']

        else:
            raise PermissionDenied

        return context

    def post(self, request, *args, **kwargs):
        if request.POST['password'] == request.POST['password-conf']:
            pass

        return success_url
