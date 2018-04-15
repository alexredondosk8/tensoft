from django import forms
from captcha.fields import ReCaptchaField

class FormRegistroCliente(forms.Form):
    nombre = forms.CharField(label="Nombres", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su(s) nombres'}))
    apellidos = forms.CharField(label="Apellidos", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su(s) apellidos'}))
    cedula = forms.CharField(label="Cédula", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su número de identificación'}))
    correo = forms.EmailField(label="Correo electrónico", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder':'Ingrese su correo electrónico'}))
    captcha = ReCaptchaField(label="Validación captcha", attrs={
        'theme' : 'clean'})
