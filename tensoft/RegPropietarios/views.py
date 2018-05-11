from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from datetime import datetime
from .models import Cliente
from .forms import *
# from .utils import *

class ClientePropietario(TemplateView):
    template_name = "RegPropietarios/cliente_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientePropietario, self).get_context_data(**kwargs)
        context['form'] = FormRegistroCliente

        return context
