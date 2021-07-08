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

class ProductoForm(forms.ModelForm):
    nombre = forms.ChoiceField(choices=[["Agua","Agua"],['Proteina','Proteina'],['Oxido','Oxido'],['Creatina','Creatina'],['Glutamina','Glutamina'],['Quemador','Quemador'],['Aminos','Aminos'],['Fruta','Fruta'],['Leche','Leche'],['Extra','Extra']])
    class Meta:
        model = Producto
        fields = ("__all__")

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ("__all__")

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not valid:
            return valid
        gym = self.cleaned_data['gym']
        producto = self.cleaned_data['producto']
        try:
            Almacen.objects.get(gym = gym,producto=producto)
            self.add_error('__all__','Ya existe el Producto en el Gimnasio seleccionado')
            return False
        except Almacen.DoesNotExist:
            return True

class TraspasoForm(forms.Form):
    origen = forms.ModelChoiceField(queryset=Gimnasio.objects.all())
    destino = forms.ModelChoiceField(queryset=Gimnasio.objects.all())
    producto =forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(required=True)

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not valid:
            return valid
        origen = self.cleaned_data['origen']
        destino = self.cleaned_data['destino']
        producto = self.cleaned_data['producto']
        cantidad = self.cleaned_data['cantidad']
        if cantidad <= 0:
            self.add_error('cantidad','No se permiten valores menores o iguales a 0')
            return False
        if origen == destino:
            self.add_error('origen','No se pueden realizar traspasos a la misma sucursal')
            return False
        try:
            obj_or = Almacen.objects.get(gym = origen,producto=producto)
            obj_dst = Almacen.objects.get(gym= destino,producto=producto)
            if obj_or.existencias < cantidad:
                self.add_error('cantidad','No tiene existencias suficientes en el origen')
                return False
            return True
        except Almacen.DoesNotExist:
            self.add_error('__all__','El producto no esta asignado en alguna de las sucursales')
            return False
    
    def save(self):
        origen = self.cleaned_data['origen']
        destino = self.cleaned_data['destino']
        producto = self.cleaned_data['producto']
        cantidad = self.cleaned_data['cantidad']

        obj_or = Almacen.objects.get(gym = origen,producto=producto)
        obj_dst = Almacen.objects.get(gym= destino,producto=producto)

        obj_or.existencias -= cantidad
        obj_dst.existencias += cantidad
        obj_or.save()
        obj_dst.save()
        return 

class EntradaForm(forms.Form):
    gym = forms.ModelChoiceField(queryset=Gimnasio.objects.all())
    producto =forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(required=True)
    precio = forms.FloatField(required=False)
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not valid:
            return valid
        gym = self.cleaned_data['gym']
        producto = self.cleaned_data['producto']
        cantidad = self.cleaned_data['cantidad']
        precio = self.cleaned_data['precio']
        if cantidad < 0:
            self.add_error('cantidad','No se permiten valores menores a 0 en cantidad')
            return False
        if precio < 0:
            self.add_error('precio','No se permiten valores menores a 0 en precio')
            return False
        return True
    
    def save(self):
        gym = self.cleaned_data['gym']
        producto = self.cleaned_data['producto']
        cantidad = self.cleaned_data['cantidad']
        precio = self.cleaned_data['precio']
        try:
            gym_obj =  Almacen.objects.get(gym = gym,producto=producto)
            gym_obj.existencias += cantidad
            gym_obj.precio = precio
            gym_obj.save()
        except Almacen.DoesNotExist:
            Almacen.objects.create(gym=gym,producto=producto,existencias=cantidad,precio=precio)
        return 