from django.conf.urls import url, include
from django.contrib import admin
from inmuebles.views import *
from RegUsuarios.views import *
from propietarios.views import *


url_inmuebles = [
    url(r'^registrar/$', InmueblesCreateView.as_view(), name="registrar-inmueble"),
    url(r'^registrar/(?P<id_inmueble>[\w.@+-]+)/fotos/$', AgregarFotosInmueble.as_view(), name="registrar-fotos-inmueble"),
    url(r'^lista/$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    #url(r'^lista/(?P<estado>[\w.@+-]+)$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    url(r'^(?P<pk>[\w.@+-]+)/$', DetallesInmueble.as_view(), name='detalles-inmuebles'),
]
url_propietario = [
    url(r'^registrar$', PropietarioCreateView.as_view(), name="registrar-propietario")
]

urlpatterns_cuenta = [
    url(r'^registrar/$', UsuarioCreateView.as_view(), name="registrar-usuario"),
    # url(r'^registrar/usuario/$', UsuarioClienteCreateView.as_view(), name="registrar-usuario-cliente"),
    # url(r'^login/$', Login.as_view(), name="login-cliente"),
    # url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # url(r'^my/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente"),
    # url(r'^(?P<id_cliente>[\w.@+-]+)/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente")
]

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', Inicio.as_view(), name='inicio'),
    url(r'^cuenta/', include(urlpatterns_cuenta)),
    url(r'^registrar-mensaje/', admin.site.urls),
=======
    url(r'^inmuebles/', include(url_inmuebles)),
    url(r'^registrar/$', ClienteUsuario.as_view(), name="registrar-usuario"),
    url(r'^propietarios/', include(url_propietario)),
>>>>>>> b8e256793383a38378ce78562daf4013af74c88c
]
