from django import forms
from .models import *

class EquipoForm(forms.ModelForm):    
    class Meta:
        model = Equipo
        fields = ('__all__')



class ReporteCreateForm(forms.ModelForm):
    id_reporte = forms.IntegerField(required=False)
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta:
        model = Reporte
        exclude = ["costo"]

class ReporteUpdateForm(forms.ModelForm):
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta:
        model = Reporte
        fields = ("__all__")


