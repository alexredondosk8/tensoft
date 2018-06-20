"""tensoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from inmobiliaria_tenant.views import *
from parreporter_tool.views import *
from reportes.views import *

from django.conf.urls.static import static

#from tensoft.inmobiliaria_tenant.views import RegistrarInmobiliaria

urlpatterns_cuenta = [
    url(r'^registrar/$', ClienteCreateView.as_view(), name="registrar-cliente"),
    url(r'^registrar/usuario/$', UsuarioClienteCreateView.as_view(), name="registrar-usuario-cliente"),
    url(r'^actualizar/$', ClienteUpdateView.as_view(), name="actualizar-cliente"),
    url(r'^login/$', auth_views.login, name="login-cliente"),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^my/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente"),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^(?P<id_cliente>[\w.@+-]+)/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]

urlpatterns_inmobiliarias = [
    url(r'^registrar/$', RegistrarInmobiliaria.as_view(), name="registrar-inmobiliaria"),
    url(r'^pendientes-alta/$', InmobiliariasPendientesAprobacionAlta.as_view(), name="inmobiliarias-pendientes-alta"),
    url(r'^pendientes-baja/$', InmobiliariasPendientesAprobacionBaja.as_view(), name="inmobiliarias-pendientes-baja"),
    url(r'^activas/$', login_required(InmobiliariasActivas.as_view()), name="inmobiliarias-activas"),
    url(r'^inactivas/$', login_required(InmobiliariasInactivas.as_view()), name="inmobiliarias-inactivas"),
    url(r'^rechazadas/$', login_required(InmobiliariasRechazadas.as_view()), name="inmobiliarias-rechazadas"),
    url(r'^(?P<id>[\w.@+-]+)/$', login_required(DetallesInmobiliaria.as_view()), name="detalles-inmobiliaria")
]

urlpatterns_dev = [
    #url(r'^$', )
    url(r'^reportar/$', login_required(ReportarProblema.as_view()), name="reportar-problema"),
    url(r'^lista/abiertas$', login_required(ListaProblemasActivos.as_view()), name="listar-problema"),
]

urlpatterns_reportes = [
    url(r'^sexo-clientes/', ReporteSexoClientesRegistrados.as_view(), name="reporte-sexo-clientes"),
    url(r'^edad-clientes/', ReporteEdadClientesRegistrados.as_view(), name="reporte-edad-clientes"),
]

urlpatterns = [
    url(r'^$', Inicio.as_view(), name='inicio'),
    url(r'^admin/', admin.site.urls),
    url(r'^cuenta/', include(urlpatterns_cuenta)),
    url(r'^inmobiliarias/', include(urlpatterns_inmobiliarias)),
    url(r'^reportes/', include(urlpatterns_reportes)),
    url(r'^dev/', include(urlpatterns_dev)),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
