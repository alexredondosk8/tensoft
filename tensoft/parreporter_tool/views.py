import os
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import ReportarInconveniente
from inmobiliaria_tenant.models import *
from .forms import *

# Create your views here.
class ReportarProblema(CreateView):
    model = ReportarInconveniente
    fields = ['prioridad', 'mensaje', 'imagen', 'desarrollador']
    success_url = "/"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ReportarProblema, self).get_form(form_class)
        form.fields['desarrollador'].initial = self.request.user.id
        form.fields['desarrollador'].disabled = True
        return form

    def form_valid(self, form):
        reporte = form.instance
        mensaje = reporte.mensaje
        imagen = reporte.imagen
        self.object = form.save()

        desarrollador = Cliente.objects.get(usuario=self.request.user)

        mensaje_completo = "Nuevas novedades de " + desarrollador.nombre + "(" + desarrollador.correo + ")"
        mensaje_completo += "\nInconvenientes reportados: " + mensaje

        email = EmailMessage (
            'Novedades en TenSoft',
            mensaje_completo,
            'soporte.tensoft@gmail.com',
            ['anderson.enriquez@correounivalle.edu.co'],
        )

        url = settings.MEDIA_ROOT + self.object.imagen.url
        print(url)

        email.attach_file(url)
        email.send()

        """send_mail(
            'Novedades en TenSoft',
            mensaje_completo,
            'soporte.tensoft@gmail.com',
            ['anderson.enriquez@correounivalle.edu.co'],
            fail_silently=False,
        )"""

        return render(self.request, "app/index.html")
