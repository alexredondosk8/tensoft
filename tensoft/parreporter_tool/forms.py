from django import forms

class FormReporteProblema(forms.Form):
    opt_prioridades = (
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta')
    )
    prioridad = forms.ChoiceField(choices=opt_prioridades)
    mensaje = forms.CharField()
    imagen = forms.ImageField(widget=forms.TextInput(attrs={
        'required': 'required'
    }))
    desarrollador = forms.CharField(widget=forms.TextInput(attrs={
        'readonly':'readonly'
    }))
