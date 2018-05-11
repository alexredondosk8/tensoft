from django.conf.urls import include, url
from django.contrib import admin
#from mensajes.views import MensajeCreateView

urlpatterns = [
    url(r'^registrar-propietarios/', include('RegPropietarios.urls')),
    url(r'^registrar-mensaje/', admin.site.urls),
]
