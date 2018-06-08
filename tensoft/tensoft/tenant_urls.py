from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from inmuebles.views import *
from RegUsuarios.views import *
from propietarios.views import *
from tensoft.settings import *
from reportes.views import *

url_inmuebles = [
    url(r'^registrar/$', InmueblesCreateView.as_view(success_url="/inmuebles/lista/?estado=1"), name="registrar-inmueble"),
    url(r'^registrar/(?P<id_inmueble>[\w.@+-]+)/fotos/$', AgregarFotosInmueble.as_view(),
        name="registrar-fotos-inmueble"),
    url(r'^lista/$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    url(r'^mapa/$', InmueblesMapa.as_view(), name='inmuebles-mapa'),
    #url(r'^lista/(?P<estado>[\w.@+-]+)$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    url(r'^(?P<pk>[\w.@+-]+)/$', DetallesInmueble.as_view(), name='detalles-inmueble'),
    url(r'^(?P<pk>[\w.@+-]+)/actualizar/$', ActualizarInmueble.as_view(), name='actualizar-inmueble'),
]

url_propietario = [
    url(r'^registrar$', PropietarioCreateView.as_view(), name="registrar-propietario")
]

url_reportes = [
    url(r'^lista-inmuebles/(?P<formato>(html|pdf))/(?P<id>[\w.@+-]+)/$', ReporteListaInmuebles.as_view(),
        name='reporte-lista-inmuebles'),
]

urlpatterns = [
    url(r'^inmuebles/', include(url_inmuebles)),
    url(r'^registrar/$', ClienteUsuario.as_view(), name="registrar-usuario"),
    url(r'^propietarios/', include(url_propietario)),
    url(r'^reportes/', include(url_reportes)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
