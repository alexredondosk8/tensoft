from django.conf.urls import url
from django.contrib import admin
#from mensajes.views import MensajeCreateView

urlpatterns = [
    url(r'^registrar-mensaje/', admin.site.urls),
]
