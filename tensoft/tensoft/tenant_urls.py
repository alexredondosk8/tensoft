from django.conf.urls import include, url
from django.contrib import admin
from RegUsuarios.views import *
#from mensajes.views import MensajeCreateView

urlpatterns_cuenta = [
    url(r'^registrar/$', UsuarioCreateView.as_view(), name="registrar-usuario"),
    # url(r'^registrar/usuario/$', UsuarioClienteCreateView.as_view(), name="registrar-usuario-cliente"),
    # url(r'^login/$', Login.as_view(), name="login-cliente"),
    # url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # url(r'^my/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente"),
    # url(r'^(?P<id_cliente>[\w.@+-]+)/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente")
]

urlpatterns = [
    url(r'^$', Inicio.as_view(), name='inicio'),
    url(r'^cuenta/', include(urlpatterns_cuenta)),
    url(r'^registrar-mensaje/', admin.site.urls),
]
