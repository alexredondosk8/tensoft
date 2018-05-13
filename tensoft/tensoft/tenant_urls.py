from django.conf.urls import url, include
from django.contrib import admin
from inmuebles.views import *


url_inmuebles = [
    url(r'^registrar/$', InmueblesCreateView.as_view(), name="registrar-inmueble"),
    url(r'^registrar/(?P<id_inmueble>[\w.@+-]+)/fotos/$', AgregarFotosInmueble.as_view(), name="registrar-fotos-inmueble"),
    url(r'^lista/$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    #url(r'^lista/(?P<estado>[\w.@+-]+)$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    url(r'^(?P<pk>[\w.@+-]+)/$', DetallesInmueble.as_view(), name='detalles-inmuebles'),
]
urlpatterns = [
    url(r'^inmuebles/', include(url_inmuebles)),
]
