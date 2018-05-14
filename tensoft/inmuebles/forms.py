from django import forms

class FormRegistrarFoto(forms.Form):
    imagen = forms.FileField(label="Seleccione las imágenes a cargar (puede subir varias)",
                            widget=forms.ClearableFileInput(attrs={'multiple': True}))
