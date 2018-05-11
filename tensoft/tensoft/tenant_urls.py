from django.conf.urls import include, url
from django.contrib import admin
from RegUsuarios.views import *
#from mensajes.views import MensajeCreateView

urlpatterns = [
    url(r'^registrar/$', ClienteUsuario.as_view(), name="registrar-usuario"),
    url(r'^registrar-mensaje/', admin.site.urls),
]
