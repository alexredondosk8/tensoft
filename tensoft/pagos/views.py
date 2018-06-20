from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from paypal.standard.forms import PayPalPaymentsForm
from datetime import datetime
from .models import *
from RegUsuarios.models import Usuario
from inmuebles.models import Inmueble

@csrf_exempt
def payment_done(request):
    factura = PagosInmueble.objects.get(numero_factura=request.GET['id_factura'])

    factura.pagada = True
    factura.fecha_pago = datetime.now()
    factura.diferencia_dias_pago = (factura.fecha_limite_pago - datetime.now().date()).days

    factura.save()

    return render(request, "pagos/done.html")

@csrf_exempt
def payment_cancelled(request):
    return render(request, "pagos/cancelled.html")

def payment_process(request):

    print(request)
    factura = PagosInmueble.objects.get(numero_factura=request.GET['id_factura'])
    print(factura.valor_pago)
    host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": factura.valor_pago,
        "item_name": factura,
        "invoice": str(factura.numero_factura),
        "currency_code": factura.get_tipo_moneda(),
        "notify_url": "http://{}{}".format(host, reverse('paypal-ipn')),
        "return_url": "http://{}{}".format(host, reverse("payment:done")+"?id_factura="+str(factura.numero_factura)),
        "cancel_return": "http://{}{}".format(host, reverse('payment:cancelled')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "form": form,
        "order": str(factura.numero_factura),
    }
    return render(request, "pagos/pago.html", context)

class ConsultarFacturas(TemplateView):
    template_name="pagos/consultar_facturas.html"

    def get_context_data(self, **kwargs):
        context = super(ConsultarFacturas, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name='usuario-inmobiliaria').exists():
            usuario_inmobiliaria = Usuario.objects.get(correo=self.request.user.username)
            facturas_x_pagar = PagosInmueble.objects.filter(
                usuario=usuario_inmobiliaria, pagada=False).order_by('fecha_limite_pago')
            context['campos'] = [
                'Número de factura',
                'Periodo facturado',
                'Valor',
                'Fecha límite de pago',
                'Dirección inmueble',
                'Tipo de transacción',
                'Acciones',
            ]
            context['facturas'] = facturas_x_pagar

            return context

class ConsultarFacturasPagadas(TemplateView):
    template_name="pagos/historico_facturas.html"

    def get_context_data(self, **kwargs):
        context = super(ConsultarFacturasPagadas, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name='usuario-inmobiliaria').exists():
            usuario_inmobiliaria = Usuario.objects.get(correo=self.request.user.username)
            facturas_x_pagar = PagosInmueble.objects.filter(
                usuario=usuario_inmobiliaria, pagada=True).order_by('fecha_limite_pago')
            context['campos'] = [
                'Número de factura',
                'Periodo facturado',
                'Valor',
                'Fecha límite de pago',
                'Fecha de pago',
                'Dirección inmueble',
                'Tipo de transacción',
                'Acciones',
            ]
            context['facturas'] = facturas_x_pagar

            return context

class DetalleFactura(DetailView):
    model = PagosInmueble
