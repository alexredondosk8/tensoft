from django.conf.urls import url, include
from django.contrib import admin
from inmuebles.views import *
from propietarios.views import *


url_inmuebles = [
    url(r'^registrar$', InmueblesCreateView.as_view(), name="registrar-inmueble"),
    url(r'^registrar/(?P<id_inmueble>[\w.@+-]+)/fotos/$', AgregarFotosInmueble.as_view(), name="registrar-fotos-inmueble"),
]
url_propietario = [
    url(r'^registrar$', PropietarioCreateView.as_view(), name="registrar-propietario")
]

urlpatterns = [
    url(r'^inmuebles/', include(url_inmuebles)),
    url(r'^propietarios/', include(url_propietario)),
]
