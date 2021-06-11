from mantto.forms import UsuarioCreacionForm
from mantto.models import FotoReporte, FotosEquipo
from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import *


class AdministracionCheck(UserPassesTestMixin):
    def test_func(self):
        return True if self.request.user.perfil.rol == Rol.objects.get(nombre='Administrador') else False

# Create your views here.
class BaseView(TemplateView):
    mantto_obj = Rol.objects.get(nombre='Mantenimiento')
    admin_obj = Rol.objects.get(nombre='Administrador')    

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
        context["equipos"] = Equipo.objects.all()
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
        context['form'].fields['asignado'].queryset = Perfil.objects.filter(rol = self.mantto_obj)
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
    action = 'reporte_detalles'

    def get(self,request,id,*args, **kwargs):
        context = self.get_context_data()
        context['reporte'] = get_object_or_404(Reporte,pk=id)
        context['equipo'] = context['reporte'].equipo
        context['title'] = f'Reporte: {id}'
        context['fotosequipo'] = FotosEquipo.objects.filter(equipo=context['reporte'].equipo)
        context['fotos_facturas'] = FotoNotaReporte.objects.filter(reporte=context['reporte'])
        context['fotos'] = FotoReporte.objects.filter(reporte__pk=id)
        context['action'] = reverse_lazy(self.action, kwargs={ 'id': context['reporte'].pk})
        context['form'] = self.form(instance=context['reporte'])
        context['form'].fields['reporto'].disabled=True
        context['form'].fields['equipo'].disabled = True
        context['form'].fields['gym'].disabled = True
        if request.user.perfil.rol != self.admin_obj:
            context['form'].fields['falla'].disabled = True
        
        if request.user.perfil.rol == self.mantto_obj:
            context['form'].fields['asignado'].disabled = True


        return render(request,self.template_name,context)
    
    def post(self,request,id,*args, **kwargs):
        form = self.form(request.POST,instance=get_object_or_404(Reporte,pk=id))
        form.fields['reporto'].disabled=True
        form.fields['equipo'].disabled = True
        form.fields['gym'].disabled = True
        if request.user.perfil.rol != self.admin_obj:
            form.fields['falla'].disabled = True
            
        if request.user.perfil.rol == self.mantto_obj:
            form.fields['asignado'].disabled = True

        if form.is_valid():
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
            
            if request.FILES:
                for file in self.request.FILES.getlist('fotos'):
                    foto = FotoReporte(reporte=reporte,img=file)
                    foto.save()
                for file in self.request.FILES.getlist('fotos_facturas'):
                    foto = FotoNotaReporte(reporte=reporte,img=file)
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
        print(id)
        reporte.delete()
        return JsonResponse({'msg': 'Eliminacion Correcta'})


class ReporteFotosView(BaseView):
    template_name = 'mantto/forms/reporte_fotos_modal.html'

    def get(self,request,id,*args, **kwargs):
        context = self.get_context_data()
        context['fotos'] = FotoReporte.objects.filter(reporte=get_object_or_404(Reporte,pk=id))
        context['title'] = f'Fotos del Reporte: {id}'
        return render(request,self.template_name,context)


class AdminMenuView(AdministracionCheck,BaseView):
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
            profile = Perfil(user = user, rol = form.cleaned_data['rol'])
            profile.save()
            return redirect(reverse('administracion_usuarios'))
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)
