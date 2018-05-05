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
from django.conf.urls.static import static

urlpatterns_cuenta = [
    url(r'^registrar/$', ClienteCreateView.as_view(), name="registrar-cliente"),
    url(r'^registrar/usuario/$', UsuarioClienteCreateView.as_view(), name="registrar-usuario-cliente"),
    url(r'^login/$', Login.as_view(), name="login-cliente"),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

urlpatterns_inmobiliarias = [
    url(r'^registrar/$', RegistrarInmobiliaria.as_view(), name="registrar-inmobiliaria"),
    url(r'^pendientes/$', InmobiliariasPendientes.as_view(), name="inmobiliarias-pendientes"),
]

urlpatterns_dev = [
    #url(r'^$', )
    url(r'^reportar/$', login_required(ReportarProblema.as_view()), name="reportar-problema"),
    #url(r'^reportar/$', CerrarProblema.as_view(), name="cerrar-problema")
]

urlpatterns = [
    url(r'^$', Inicio.as_view(), name='inicio'),
    url(r'^admin/', admin.site.urls),
    url(r'^cuenta/', include(urlpatterns_cuenta)),
    url(r'^inmobiliarias/', include(urlpatterns_inmobiliarias)),
    url(r'^dev/', include(urlpatterns_dev)),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
