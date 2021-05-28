from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()
router.register('reportes',ReporteViewSet)

urlpatterns = [
    path('home/',login_required(views.homeView.as_view()),name='home'),

    # [------------- MANTENIMIENTO --------------] # 
    path('mantenimiento/',login_required(views.ManttoMenuView.as_view()),name="mantenimiento"),
    path('mantenimiento/equipo/agregar/',login_required(views.EquipoAddView.as_view()),name="equipo_agregar"),
    path('mantenimiento/equipo/',login_required(views.EquipoListView.as_view()),name="equipo_lista"),
    path('mantenimiento/reporte/crear/<int:id_equipo>/',login_required(views.ReporteAddView.as_view()),name="reporte_crear"),
    path('mantenimiento/reporte/',login_required(views.ReporteListView.as_view()),name="reportes"),
    path('mantenimiento/reporte/<int:id>/',login_required(views.ReporteDetailsView.as_view()),name="reporte_detalles"),
    path('api/',include(router.urls))
] 