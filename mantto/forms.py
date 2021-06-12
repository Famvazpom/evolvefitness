from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UsuarioCreacionForm(UserCreationForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','rol','password1','password2']

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UsuarioCreacionForm, self).save(commit=True)
        return user

class EquipoForm(forms.ModelForm):    
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta:
        model = Equipo
        fields = ('__all__')

class EquipoUpdateForm(forms.ModelForm):    
    id_equipo = forms.IntegerField(required=False)
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta:
        model = Equipo
        fields = ('__all__')


class ReporteCreateForm(forms.ModelForm):
    id_reporte = forms.IntegerField(required=False)
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    asignado= forms.ModelMultipleChoiceField(queryset=Perfil.objects.filter(rol=Rol.objects.get(nombre='Mantenimiento')),
            widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Reporte
        exclude = ["costo","tipopago",'mensajes']
        widgets = {
          'falla': forms.Textarea(attrs={'rows':4}),
        }

class ReporteUpdateForm(forms.ModelForm):
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    fotos_facturas = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,}),required=False)
    asignado= forms.ModelMultipleChoiceField(queryset=Perfil.objects.filter(rol=Rol.objects.get(nombre='Mantenimiento')),
            widget=forms.CheckboxSelectMultiple)

    diagnostico = forms.CharField(widget=forms.Textarea(attrs={'rows':4}),required=False)
    class Meta:
        model = Reporte
        exclude = ["revisado",'mensajes']
        widgets = {
          'falla': forms.Textarea(attrs={'rows':4}),
        }

    def __init__(self,*args,**kwargs):
        super(ReporteUpdateForm,self).__init__(*args, **kwargs)
        self.fields['diagnostico'].label = 'Reparación/Nueva Falla'
        self.fields['fotos_facturas'].label = 'Fotos de Notas / Facturas'
    


