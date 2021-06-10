from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()
router.register('reportes',ReporteViewSet)
router.register('foto-reporte',FotoReporteViewSet)

urlpatterns = [
    path('home/',login_required(views.homeView.as_view()),name='home'),

    # [------------- MANTENIMIENTO --------------] # 
    path('mantenimiento/',login_required(views.ManttoMenuView.as_view()),name="mantenimiento"),
    path('mantenimiento/equipo/agregar/',login_required(views.EquipoAddView.as_view()),name="equipo_agregar"),
    path('mantenimiento/equipo/actualizar/<int:id_equipo>/',login_required(views.EquipoUpdateView.as_view()),name="equipo_actualizar"),
    path('mantenimiento/equipo/',login_required(views.EquipoListView.as_view()),name="equipo_lista"),
    path('mantenimiento/reporte/crear/<int:id_equipo>/',login_required(views.ReporteAddView.as_view()),name="reporte_crear"),
    path('mantenimiento/reporte/',login_required(views.ReporteListView.as_view()),name="reportes"),
    path('mantenimiento/reporte/detalles/<int:id>/',login_required(views.ReporteDetailsView.as_view()),name="reporte_detalles"),
    path('mantenimiento/reporte/eliminar/<int:id>/',login_required(views.ReporteDeleteView.as_view()),name="reporte_eliminar"),
    path('mantenimiento/reporte/fotos/<int:id>/',login_required(views.ReporteFotosView.as_view()),name="reporte_fotos"),
    path('administracion/',login_required(views.AdminMenuView.as_view()),name="administracion"),
    path('administracion/usuarios/',login_required(views.UserListView.as_view()),name="administracion_usuarios"),
    path('administracion/usuarios/crear/',login_required(views.UserCreateView.as_view()),name="administracion_usuarios_crear"),
    path('api/',include(router.urls))
] 