from django import forms
from captcha.fields import ReCaptchaField

class FormRegistroCliente(forms.Form):
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su(s) nombres'
    }))
    apellidos = forms.CharField(label="Apellidos", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su(s) apellidos'
    }))
