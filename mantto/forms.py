from django import forms
from .models import *

class EquipoForm(forms.ModelForm):    
    class Meta:
        model = Equipo
        fields = ('__all__')



class ReporteCreateForm(forms.ModelForm):
    id_reporte = forms.IntegerField(required=False)
    class Meta:
        model = Reporte
        exclude = ["costo"]

class ReporteUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Reporte
        fields = ("__all__")


