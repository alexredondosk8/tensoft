from django import forms
from .models import *
from captcha.fields import ReCaptchaField


SEXO_CHOICES = (
    (1, "Femenino"),
    (2, "Masculino"),
)

YEARS_CHOICES = (
    '1916', '1917', '1918', '1919', '1920', '1921', '1922', '1923',
    '1924', '1925', '1926', '1927', '1928', '1929', '1930', '1931',
    '1932', '1933', '1934', '1935', '1936', '1937', '1938', '1939',
    '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947',
    '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955',
    '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963',
    '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971',
    '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
    '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
    '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
    '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
    '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
    '2012', '2013', '2014', '2015', '2016', '2017', '2018')
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
    sexo = forms.ChoiceField(label="Sexo", choices=SEXO_CHOICES)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.SelectDateWidget(
        years=YEARS_CHOICES
    ))
    correo = forms.EmailField(label="Correo electrónico", widget=forms.TextInput(attrs={
        'class': 'item form-control',
        'placeholder':'Ingrese su correo electrónico'}))
    captcha = ReCaptchaField(label="Validación captcha", attrs={
        'theme' : 'clean'})

class FormUpdateCliente(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos']
