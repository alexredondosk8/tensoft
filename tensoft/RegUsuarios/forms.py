from django import forms
from .models import *
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
    cedula = forms.CharField(label="Cédula", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su número de identificación'}))
    correo = forms.EmailField(label="Correo electrónico", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder':'Ingrese su correo electrónico'}))
    telefono = forms.CharField(label="Teléfono", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su número de teléfono'}))
    celular = forms.CharField(label="Celular", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su número de celular'}))
    captcha = ReCaptchaField(label="Validación captcha", attrs={
        'theme' : 'clean'})

class FormUpdateCliente(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos']
