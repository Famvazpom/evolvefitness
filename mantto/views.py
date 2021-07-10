from django.db.models import query
from mantto.models import FotoReporte, FotosEquipo
from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse, request
from django.views.generic.base import TemplateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms.models import modelformset_factory
import json
from .forms import *


class AdministracionCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.perfil.rol in [
            Rol.objects.get(nombre='Administrador'),
            Rol.objects.get(nombre='Gerencia'),
        ]

class AdministracionRecepcionCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.perfil.rol in [
            Rol.objects.get(nombre='Administrador'),
            Rol.objects.get(nombre='Gerencia'),
            Rol.objects.get(nombre='Recepcionista'),
        ]

class AdministracionContadorRecepcionCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.perfil.rol in [
            Rol.objects.get(nombre='Administrador'),
            Rol.objects.get(nombre='Gerencia'),
            Rol.objects.get(nombre='Recepcionista'),
            Rol.objects.get(nombre='Contabilidad'),
        ]

# Create your views here.
class BaseView(TemplateView):
    mantto_obj = Rol.objects.get(nombre='Mantenimiento')
    admin_obj = Rol.objects.get(nombre='Administrador')  
    recep_obj = Rol.objects.get(nombre="Recepcionista")  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = 'Mantenimiento'
        return context

class homeView(BaseView):
    template_name = 'mantto/main_menu.html'


class ManttoMenuView(BaseView):
    template_name = "mantto/mantenimiento_menu.html"

class EquipoAddView(AdministracionCheck,BaseView):
    template_name = "mantto/forms/equipo_add.html"
    form = EquipoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form()
        return context

    def post(self,request,*args, **kwargs):
        form = self.form(request.POST,request.FILES)

        if form.is_valid():
            equipo = form.save()
            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    foto = FotosEquipo(equipo=equipo,img=file)
                    foto.save()
            return redirect(reverse('mantenimiento'))
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request,self.template_name,context)

class EquipoListView(BaseView):
    template_name = 'mantto/reportes/equipo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gyms'] = Gimnasio.objects.all()
        return context

class EquipoUpdateView(BaseView):
    template_name = 'mantto/forms/equipo_actualizar.html'
    form = EquipoUpdateForm
    action = 'equipo_actualizar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Actualizar Equipo'
        return context

    def get(self,request,id_equipo,*args, **kwargs):
        context = self.get_context_data()
        equipo =  get_object_or_404(Equipo,pk=id_equipo)
        context["form"] = self.form(instance=equipo)
        context['form'].fields['id_equipo'].initial = equipo.pk
        context['form'].fields['id_equipo'].disabled = True
        context['fotosequipo'] = FotosEquipo.objects.filter(equipo__pk=id_equipo)
        context['action'] = reverse_lazy(self.action, kwargs={'id_equipo':id_equipo})
        return render(request,self.template_name,context)

    def post(self,request,id_equipo,*args, **kwargs):
        equipo = get_object_or_404(Equipo,pk=id_equipo)
        form = self.form(request.POST,instance = equipo)
        if form.is_valid():
            equipo = form.save()
            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    FotosEquipo.objects.create(equipo=equipo,img=file)
            return redirect(reverse('equipo_lista'))
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ReporteAddView(BaseView):
    template_name = 'mantto/forms/reporte_add.html'
    form = ReporteCreateForm
    action = 'reporte_crear'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Reportar Equipo'
        context["form"] = self.form()
        return context

    def get(self,request,id_equipo,*args, **kwargs):
        context = self.get_context_data()
        context['equipo'] = get_object_or_404(Equipo,pk=id_equipo)
        context['fotosequipo'] = FotosEquipo.objects.filter(equipo__pk=id_equipo)
        context['action'] = reverse_lazy(self.action, kwargs={'id_equipo':id_equipo})
        context['form'].fields['equipo'].initial = context['equipo']
        context['form'].fields['gym'].initial = context['equipo'].gym
        try:
            context['form'].fields['id_reporte'].initial = Reporte.objects.latest('id').pk+1
        except Reporte.DoesNotExist:
            context['form'].fields['id_reporte'].initial = 1
        context['form'].fields['reporto'].initial = request.user.perfil
        context['form'].fields['asignado'].queryset = Perfil.objects.filter(rol = self.mantto_obj,user__is_active=True).order_by('user__first_name')
        context['form'].fields['estado'].queryset = Estado.objects.filter(nombre__in = ['No Funciona','Funcionando con detalles pendientes'])
        context['form'].fields['id_reporte'].disabled=True
        context['form'].fields['equipo'].disabled = True


        return render(request,self.template_name,context)

    def post(self,request,id_equipo,*args, **kwargs):
        form = self.form(request.POST)
        equipo = get_object_or_404(Equipo,pk=id_equipo)
        form.fields['equipo'].initial = equipo
        form.fields['gym'].initial = equipo.gym
        form.fields['reporto'].initial = request.user.perfil
        form.fields['id_reporte'].disabled=True
        form.fields['equipo'].disabled = True
        if form.is_valid():
            reporte = form.save()

            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    foto = FotoReporte(reporte=reporte,img=file)
                    foto.save()
            return redirect(reverse('equipo_lista'))
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ReporteListView(BaseView):
    template_name = 'mantto/reportes/reporte_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = Estado.objects.all()
        context['gyms'] = Gimnasio.objects.all()
        context['asignado'] = Perfil.objects.filter(rol__nombre='Mantenimiento')
        return context

class ReporteDetailsView(BaseView):
    template_name = 'mantto/forms/reporte_detalles_modal.html'
    form = ReporteUpdateForm
    formset = modelformset_factory(ReporteMensaje,form=MensajeUpdateForm,extra=0)
    action = 'reporte_detalles'

    def disable_formset(self,request,formset):
        if request.user.perfil.rol != self.admin_obj:
            for i in formset:
                i.fields['mensaje'].disabled = True
                i.fields['eliminar'].disabled = True
        return formset

    def get(self,request,id,*args, **kwargs):
        context = self.get_context_data()
        context['reporte'] = get_object_or_404(Reporte,pk=id)
        context['equipo'] = context['reporte'].equipo
        context['title'] = f'Reporte: {id}'
        context['fotosequipo'] = FotosEquipo.objects.filter(equipo=context['reporte'].equipo)
        context['fotos_facturas'] = FotoNotaReporte.objects.filter(gasto__in=Gasto.objects.filter(reportes=context['reporte']))

        context['fotos'] = FotoReporte.objects.filter(reporte__pk=id)
        context['action'] = reverse_lazy(self.action, kwargs={ 'id': context['reporte'].pk})
        context['formset'] = self.disable_formset(request,self.formset(queryset=context['reporte'].mensajes.all()))
        context['form'] = self.form(instance=context['reporte'])
        context['form'].fields['reporto'].disabled=True
        context['form'].fields['equipo'].disabled = True
        context['form'].fields['gym'].disabled = True
        context['form'].fields['asignado'].queryset = Perfil.objects.filter(rol = self.mantto_obj,user__is_active=True).order_by('user__first_name')
        if request.user.perfil.rol != self.admin_obj:
            context['form'].fields['falla'].disabled = True
        
        if request.user.perfil.rol == self.mantto_obj:
            context['form'].fields['asignado'].disabled = True

        return render(request,self.template_name,context)
    
    def post(self,request,id,*args, **kwargs):
        form = self.form(request.POST,instance=get_object_or_404(Reporte,pk=id))
        formset = self.disable_formset(request,self.formset(request.POST,queryset=get_object_or_404(Reporte,pk=id).mensajes.all()))
        form.fields['reporto'].disabled=True
        form.fields['equipo'].disabled = True
        form.fields['gym'].disabled = True
        if request.user.perfil.rol != self.admin_obj:
            form.fields['falla'].disabled = True
        if request.user.perfil.rol == self.mantto_obj:
            form.fields['asignado'].disabled = True

        if form.is_valid() and formset.is_valid():
            reporte = form.save()
            if reporte.asignado == request.user.perfil:
                reporte.revisado = True
                reporte.save()
            dg = form.cleaned_data['diagnostico']
            if dg:
                mensaje = ReporteMensaje(reporte=reporte,mensaje=dg,autor=request.user.perfil)
                mensaje.save()
                reporte.mensajes.add(mensaje)
                reporte.save()
            for item in formset:
                item.save()
            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    foto = FotoReporte(reporte=reporte,img=file)
                    foto.save()
            return redirect(reverse('reportes'))
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ReporteDeleteView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/reporte_eliminar_modal.html'
    action = 'reporte_eliminar'

    def get(self,request,id,*args, **kwargs):
        context = self.get_context_data()
        context['title'] = f'Eliminar Reporte: {id}'
        context['action'] = reverse_lazy(self.action, kwargs={'id':id})
        return render(request,self.template_name,context)
    
    def post(self,request,id, *args,**kwargs):
        reporte = Reporte.objects.get(pk=id)
        for i in reporte.mensajes.all():
            i.delete()
        reporte.delete()
        return redirect(reverse('reportes'))

class ReporteFotoDeleteView(AdministracionCheck,BaseView):
    
    def post(self,request,id, *args,**kwargs):
        reporte = FotoReporte.objects.get(pk=id)
        reporte.delete()
        return JsonResponse({'msg': 'Eliminacion Correcta'})

class ReporteFotoNotaDeleteView(AdministracionCheck,BaseView):
    
    def post(self,request,id, *args,**kwargs):
        reporte = FotoNotaReporte.objects.get(pk=id)
        reporte.delete()
        return JsonResponse({'msg': 'Eliminacion Correcta'})

class ReporteFotosView(BaseView):
    template_name = 'mantto/forms/reporte_fotos_modal.html'

    def get(self,request,id,*args, **kwargs):
        context = self.get_context_data()
        context['fotos'] = FotoReporte.objects.filter(reporte=get_object_or_404(Reporte,pk=id))
        context['title'] = f'Fotos del Reporte: {id}'
        return render(request,self.template_name,context)

## Menu de administracion

class AdminMenuView(AdministracionContadorRecepcionCheck,BaseView):
    template_name = "mantto/administracion_menu.html"

class UserListView(AdministracionCheck,BaseView):
    template_name = "mantto/admin/usuarios.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['usuarios'] = Perfil.objects.all()
        return context

class UserCreateView(AdministracionCheck,BaseView):
    template_name = "mantto/forms/usuario_crear.html"
    form = UsuarioCreacionForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['title'] = 'Crear usuario'
        context['action'] = reverse_lazy('administracion_usuarios_crear')
        return context
    
    def post(self,request, *args,**kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Perfil(user = user, rol = form.cleaned_data['rol'],gym = form.cleaned_data['gym'])
            profile.save()
            return redirect(reverse('administracion_usuarios'))
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class UserUpdateView(AdministracionCheck,BaseView):
    template_name = "mantto/forms/usuario_actualizar.html"
    form = PerfilActualizarForm

    def get_context_data(self,usr, **kwargs):
        context =  super().get_context_data(**kwargs)
        obj = User.objects.get(username=usr)
        context['title'] = f'Actualizar usuario {obj.perfil}'
        context['form'] = self.form(instance=obj)
        context['form'].fields['rol'].initial = obj.perfil.rol
        context['form'].fields['gym'].initial = obj.perfil.gym
        context['action'] = reverse_lazy('administracion_usuarios_actualizar', kwargs={'usr': obj.username})
        return context
    
    def get(self,request,usr,*args, **kwargs):
        context = self.get_context_data(usr)
        return render(request,self.template_name,context)

    def post(self,request,usr,*args, **kwargs):
        obj = User.objects.get(username=usr)
        form = self.form(request.POST,instance=obj)
        
        if form.is_valid():
            form.save()
            obj.perfil.rol = form.cleaned_data['rol']
            obj.perfil.gym = form.cleaned_data['gym']
            obj.perfil.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            print(form.errors)
            return JsonResponse(data=errors, status=400)

class UserPasswordUpdateView(AdministracionCheck,BaseView):
    template_name = "mantto/forms/usuario_crear.html"
    form = UserPasswordChangeForm

    def get_context_data(self,usr, **kwargs):
        context =  super().get_context_data(**kwargs)
        obj = User.objects.get(username=usr)
        context['title'] = f'Actualizar usuario {obj.perfil}'
        context['form'] = self.form(user=obj)
        context['action'] = reverse_lazy('administracion_usuarios_actualizar_pwd', kwargs={'usr': obj.username})
        return context
    
    def get(self,request,usr,*args, **kwargs):
        context = self.get_context_data(usr)
        return render(request,self.template_name,context)

    def post(self,request,usr,*args, **kwargs):
        obj = User.objects.get(username=usr)
        form = self.form(obj,request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class UserDeactivateView(AdministracionCheck,BaseView):
    def get(self,request,usr,*args, **kwargs):
        obj = User.objects.get(username=usr)
        obj.is_active = not obj.is_active
        obj.save()
        print('in')
        return redirect(reverse('administracion_usuarios'))

class SucursalCreateView(AdministracionCheck,BaseView):
    template_name = "mantto/forms/sucursal_crear.html"
    form = GimnasioCreateForm
    action = 'administracion-sucursal-crear'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form()
        context['title'] = 'Crear Gimnasio'
        context['action'] = reverse_lazy(self.action)
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ProveedorAddView(AdministracionCheck,BaseView):
    template_name='mantto/forms/proveedor_add.html'
    title= 'Registrar Proveedor'
    action = 'administracion-proveedor-agregar'
    form = ProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        context['action'] = reverse_lazy(self.action)
        context['form'] = self.form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class GastosListView(AdministracionContadorRecepcionCheck,BaseView):
    template_name = "mantto/admin/gastos_list.html"

class GastosAddView(AdministracionContadorRecepcionCheck,BaseView):
    template_name = "mantto/forms/gasto_add.html"
    title = "Registrar Gasto"
    action = 'administracion-gastos-agregar'
    form = GastoAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        context['action'] = reverse_lazy(self.action)
        context['form'] = self.form()
        return context

    def disable_fields(self,form,perfil):
        if perfil.rol not in [ Rol.objects.get(nombre='Administrador'),Rol.objects.get(nombre='Gerencia') ]:
            form.fields['pago'].queryset = Perfil.objects.filter(pk = perfil.pk)
            form.fields['pago'].initial = perfil
        if perfil.rol == self.recep_obj:
            form.fields['gym'].initial = perfil.gym
            form.fields['gym'].queryset = Gimnasio.objects.filter(pk = perfil.gym.pk )

        return
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        self.disable_fields(context['form'],request.user.perfil)
        return render(request,self.template_name,context)


    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save()
            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    foto = FotoNotaReporte(gasto=obj,img=file)
                    foto.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class GastosUpdateView(AdministracionContadorRecepcionCheck,BaseView):
    template_name = "mantto/forms/gasto_add.html"
    title = "Registrar Gasto"
    action = 'administracion-gastos-actualizar'
    form = GastoUpdateForm

    def disable_fields(self,user,form):
        if user.perfil.rol != self.admin_obj:
            form.fields['importe'].disabled = True
            form.fields['gym'].disabled= True
            form.fields['pago'].disabled= True
            form.fields['proveedor'].disabled= True
            form.fields['forma_pago'].disabled= True
            form.fields['reportes'].disabled= True
            form.fields['descripcion'].disabled= True
        return form

    def get_context_data(self,gasto, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        context['action'] = reverse_lazy(self.action,kwargs={'gasto':gasto})
        context['form'] = self.form(instance=Gasto.objects.get(pk=gasto))
        context['fotos_facturas'] = FotoNotaReporte.objects.filter(gasto=Gasto.objects.get(pk=gasto))

        return context

    def get(self, request,gasto, *args, **kwargs):
        context = self.get_context_data(gasto)
        self.disable_fields(request.user,context['form'])
        return render(request,self.template_name,context)

    def post(self, request,gasto, *args, **kwargs):
        form = self.form(request.POST,instance=Gasto.objects.get(pk=gasto))
        self.disable_fields(request.user,form)
        if form.is_valid():
            obj = form.save()
            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    foto = FotoNotaReporte(gasto=obj,img=file)
                    foto.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class GastosDeleteView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/gasto_eliminar_modal.html'
    action = 'gastos-eliminar'

    def get(self,request,id,*args, **kwargs):
        context = self.get_context_data()
        context['title'] = f'Eliminar Gasto: {id}'
        context['action'] = reverse_lazy(self.action, kwargs={'id':id})
        return render(request,self.template_name,context)
    
    def post(self,request,id, *args,**kwargs):
        reporte = Gasto.objects.get(pk=id)
        reporte.delete()
        return redirect(reverse('administracion-gastos'))

class ProductoListView(AdministracionCheck,BaseView):
    template_name = 'mantto/admin/producto_list.html'

class ProductoAddView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/producto_add.html'
    action = 'administracion-producto-crear'
    title = 'Registrar Producto'
    form = ProductoForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        context['action'] = reverse_lazy(self.action)
        context['form'] = self.form()

        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ProductoDetailsView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/producto_add.html'
    action = 'administracion-producto-modificar'
    title = 'Registrar Producto'
    form = ProductoForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        return context

    def get(self,request,producto,*args, **kwargs):
        context = self.get_context_data()
        context['action'] = reverse_lazy(self.action,kwargs = { 'producto': producto })
        context['form'] = self.form(instance=Producto.objects.get(pk=producto))
        return render(request,self.template_name,context)
    
    def post(self, request,producto, *args, **kwargs):
        form = self.form(request.POST,request.FILES,instance=Producto.objects.get(pk=producto))
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ProductoDeleteView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/producto_eliminar.html'
    action = 'administracion-producto-eliminar'
    title = 'Eliminar Producto'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        return context

    def get(self,request,producto,*args, **kwargs):
        context = self.get_context_data()
        context['action'] = reverse_lazy(self.action,kwargs = { 'producto': producto })
        return render(request,self.template_name,context)
    
    def post(self, request,producto, *args, **kwargs):
        obj = Producto.objects.get(pk=producto)
        obj.activo = not obj.activo
        obj.save()
        return redirect(reverse('administracion-productos-lista'))

class InventariosView(AdministracionRecepcionCheck,BaseView):
    template_name = 'mantto/inventario-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gyms"] = Gimnasio.objects.all()
        return context
    

class InventariosCreateView(AdministracionRecepcionCheck,BaseView):
    template_name = 'mantto/forms/inventario-crear.html'
    form = AlmacenForm
    action = 'inventarios-agregar'
    title = 'Agregar al Almacen'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title 
        context['action'] = reverse_lazy(self.action)
        context['form'] = self.form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class TraspasoView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/traspaso.html'
    form = TraspasoForm
    action = 'administracion-traspaso'
    title = 'Traspasar Articulos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form()
        context['action'] = reverse_lazy(self.action)
        context['title'] = self.title
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class EntradaProductoView(AdministracionCheck,BaseView):
    template_name = 'mantto/forms/entrada_producto.html'
    form = EntradaForm
    action = 'administracion-entrada-producto'
    title = 'Registrar Entrada'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form()
        context['action'] = reverse_lazy(self.action)
        context['title'] = self.title
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'Correcto'})
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ProductoPrecio(AdministracionCheck,BaseView):
    def get(self,request):
        gym = request.GET.get('gym')
        prod = request.GET.get('producto')
        try:
            precio = Almacen.objects.get(gym__id=gym,producto__id=prod).precio
        except Almacen.DoesNotExist:
            precio = '0.00'
        return JsonResponse({'precio':precio})

class VentaProductosView(BaseView):
    template_name = 'mantto/venta-productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = NotaVenta.objects.last()
        context["last"] = obj.id if obj else 1
        return context
    

    def descontar_almacen(self,almacen,cantidad):
        obj = Almacen.objects.get(pk=almacen)
        obj.existencias -= int(cantidad)
        obj.save()
        return obj,obj.producto
    
    def post(self,request,*args, **kwargs):
        items = json.loads(request.POST.get('productos'))
        obj = NotaVenta.objects.create(descuento = float(request.POST.get('descuento')),gym=request.user.perfil.gym)
        for item in items:
            alm,producto = self.descontar_almacen(item['id'],item['cantidad'])
            ob = ProductosNota.objects.create(nota= obj,producto=producto,cantidad=item['cantidad'],
                precio=alm.precio,costo=producto.costo)
        obj.save()
        return JsonResponse({'msg':'ok','last': obj.id+1})

class VentaProductoDetails(BaseView):
    template_name = 'mantto/forms/nota-venta-details.html'

    def get(self, request,folio, *args, **kwargs):
        context = self.get_context_data()
        obj = NotaVenta.objects.get(pk=folio)
        productos = ProductosNota.objects.filter(nota=obj)
        context['nota'] = obj
        context['title'] = f"Detalles de la Nota: {obj}"
        context['productos'] = productos
        return render(request,self.template_name,context)

class TagView(AdministracionCheck,BaseView):
    template_name = 'mantto/reportes/tag_list.html'