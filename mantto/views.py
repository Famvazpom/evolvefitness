from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.urls import reverse,reverse_lazy
from .forms import *


# Create your views here.
class BaseView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = 'Mantenimiento'
        return context

class homeView(BaseView):
    template_name = 'mantto/main_menu.html'


class ManttoMenuView(BaseView):
    template_name = "mantto/mantenimiento_menu.html"

class EquipoAddView(BaseView):
    template_name = "mantto/forms/equipo_add.html"
    form = EquipoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form()
        return context

    def post(self,request,*args, **kwargs):
        form = self.form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
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
        context['action'] = reverse_lazy(self.action, kwargs={'id_equipo':id_equipo})
        context['form'].fields['equipo'].initial = context['equipo']
        context['form'].fields['gym'].initial = context['equipo'].gym
        try:
            context['form'].fields['id_reporte'].initial = Reporte.objects.latest('id').pk+1
        except Reporte.DoesNotExist:
            context['form'].fields['id_reporte'].initial = 1
        context['form'].fields['reporto'].initial = request.user.perfil
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
            form.save()
            return redirect(reverse('equipo_lista'))
        else:
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)

class ReporteListView(BaseView):
    template_name = 'mantto/reportes/reporte_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reportes"] = Reporte.objects.all()
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
        context['action'] = reverse_lazy(self.action, kwargs={ 'id': context['reporte'].pk})
        context['form'] = self.form(instance=context['reporte'])
        
        context['form'].fields['reporto'].disabled=True
        context['form'].fields['equipo'].disabled = True
        context['form'].fields['gym'].disabled = True
        return render(request,self.template_name,context)
    
    def post(self,request,id,*args, **kwargs):
        form = self.form(request.POST,instance=get_object_or_404(Reporte,pk=id))
        form.fields['reporto'].disabled=True
        form.fields['equipo'].disabled = True
        form.fields['gym'].disabled = True
        if form.is_valid():
            form.save()
            return redirect(reverse('reportes'))
        else:
            print(form.errors)
            errors = {f: e.get_json_data() for f, e in form.errors.items()}
            return JsonResponse(data=errors, status=400)