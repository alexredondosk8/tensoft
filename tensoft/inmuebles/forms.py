from django import forms

class FormRegistrarFoto(forms.Form):
    imagen = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
