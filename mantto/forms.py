from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import *

class UsuarioCreacionForm(UserCreationForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    gym = forms.ModelChoiceField(queryset=Gimnasio.objects.all())
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','rol','password1','password2']


class GimnasioCreateForm(forms.ModelForm):
    class Meta:
        model = Gimnasio
        fields = ('__all__')

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
    gym = forms.ModelChoiceField(queryset=Gimnasio.objects.all().order_by('nombre'))

    class Meta:
        model = Reporte
        exclude = ["costo","tipopago",'mensajes']
        widgets = {
          'falla': forms.Textarea(attrs={'rows':2}),
        }

class MensajeUpdateForm(forms.ModelForm):
    eliminar = forms.BooleanField(required=False)
    class Meta:
        model= ReporteMensaje
        fields = ('mensaje','eliminar')
        widgets = {
          'mensaje': forms.Textarea(attrs={'rows':2,'required':False}),
        }
    def save(self, commit=True):
        instance = super(MensajeUpdateForm, self).save(commit=False)
        if commit:
            if self.cleaned_data['eliminar']:
                instance.delete() 
            else:
                instance.save()
            
        return instance

class ReporteUpdateForm(forms.ModelForm):
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    diagnostico = forms.CharField(widget=forms.Textarea(attrs={'rows':4}),required=False)
    class Meta:
        model = Reporte
        exclude = ["revisado",'mensajes']
        widgets = {
          'falla': forms.Textarea(attrs={'rows':2}),
        }

    def __init__(self,*args,**kwargs):
        super(ReporteUpdateForm,self).__init__(*args, **kwargs)
        self.fields['diagnostico'].label = 'Reparación/Nueva Falla'
    
class PerfilActualizarForm(forms.ModelForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    gym = forms.ModelChoiceField(queryset=Gimnasio.objects.all())
    class Meta:
        model= User
        fields = ['first_name','last_name']

class UserPasswordChangeForm(AdminPasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

class GastoAddForm(forms.ModelForm):
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all().order_by('nombre'),required=False)
    pago = forms.ModelChoiceField(queryset=Perfil.objects.exclude(rol__in=[
        Rol.objects.get(nombre='Mantenimiento'),
        Rol.objects.get(nombre='Proveedor')
        ],).order_by('user__first_name'))
    gym = forms.ModelChoiceField(queryset=Gimnasio.objects.all().order_by('nombre'))
    forma_pago = forms.ModelChoiceField(queryset=TipoPagoReporte.objects.all().order_by('nombre'))
    class Meta:
        model = Gasto
        fields = ("__all__")

    def __init__(self,*args, **kwargs):
        super(GastoAddForm,self).__init__(*args, **kwargs)
        self.fields['fotos'].label = 'Fotos de Notas/Facturas'

class GastoUpdateForm(forms.ModelForm):
    fotos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all().order_by('nombre'),required=False)
    pago = forms.ModelChoiceField(queryset=Perfil.objects.exclude(rol__in=[
        Rol.objects.get(nombre='Mantenimiento'),
        Rol.objects.get(nombre='Proveedor')
        ],).order_by('user__first_name'))
    gym = forms.ModelChoiceField(queryset=Gimnasio.objects.all().order_by('nombre'))
    forma_pago = forms.ModelChoiceField(queryset=TipoPagoReporte.objects.all().order_by('nombre'))

    class Meta:
        model = Gasto
        fields = ("__all__")
    
    def __init__(self,*args, **kwargs):
        super(GastoUpdateForm,self).__init__(*args, **kwargs)
        self.fields['fotos'].label = 'Fotos de Notas/Facturas'

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ("__all__")
