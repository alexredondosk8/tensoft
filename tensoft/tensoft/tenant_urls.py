from django.conf.urls import include, url
from django.contrib import admin
from RegPropietarios.views import *
#from mensajes.views import MensajeCreateView

urlpatterns = [
    url(r'^registrar/$', ClientePropietario.as_view(), name="registrar-cliente"),
    url(r'^registrar-mensaje/', admin.site.urls),
]
