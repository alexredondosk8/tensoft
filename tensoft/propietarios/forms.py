from django import forms
from .models import *

class FormRegistroPropietario(forms.Form):

    identificacion = forms.CharField(label="Identificacion", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su número de identificación'}))

    nombres = forms.CharField(label="Nombres", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su(s) nombres'}))
    apellidos = forms.CharField(label="Apellidos", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su(s) apellidos'}))

    direccion = forms.CharField(label="Direccion", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su direccion de residencia'}))

    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder': 'Ingrese su número de telefono o celular'}))

    email = forms.EmailField(label="Correo electrónico", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder':'Ingrese su correo electrónico'}))

class FormUpdatePropietario(forms.ModelForm):

    class Meta:
        model = Propietario
        fields = ['identificacion', 'nombres', 'apellidos', 'direccion', 'telefono', 'email']