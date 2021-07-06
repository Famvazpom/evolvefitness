from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()
router.register('reportes',ReporteViewSet)
router.register('equipos',EquipoViewSet)
router.register('foto-reporte',FotoReporteViewSet)
router.register('gastos',GastoViewSet)
router.register('proveedores',ProveedorViewSet)
router.register('productos',ProductoViewSet)
router.register('almacenes',AlmacenViewSet)

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
    path('mantenimiento/reporte/fotos/eliminar/<int:id>/',login_required(views.ReporteFotoDeleteView.as_view()),name="reporte_foto_eliminar"),
    path('mantenimiento/reporte/nota/eliminar/<int:id>/',login_required(views.ReporteFotoNotaDeleteView.as_view()),name="reporte_foto_nota_eliminar"),


    # [------------- ADMINISTRACION --------------] # 
    path('administracion/',login_required(views.AdminMenuView.as_view()),name="administracion"),
    path('administracion/gastos/',login_required(views.GastosListView.as_view()),name="administracion-gastos"),
    path('administracion/gastos/add/',login_required(views.GastosAddView.as_view()),name="administracion-gastos-agregar"),
    path('administracion/gastos/actualizar/<int:gasto>',login_required(views.GastosUpdateView.as_view()),name="administracion-gastos-actualizar"),
    path('administracion/gastos/elminiar/<int:id>',login_required(views.GastosDeleteView.as_view()),name="gastos-eliminar"),

    path('administracion/productos/',login_required(views.ProductoListView.as_view()),name="administracion-productos-lista"),
    path('administracion/productos/agregar/',login_required(views.ProductoAddView.as_view()),name="administracion-producto-crear"),
    path('administracion/productos/modificar/<int:producto>',login_required(views.ProductoDetailsView.as_view()),name="administracion-producto-modificar"),
    path('administracion/productos/eliminar/<int:producto>',login_required(views.ProductoDeleteView.as_view()),name="administracion-producto-eliminar"),

    path('administracion/proveedor/add/',login_required(views.ProveedorAddView.as_view()),name="administracion-proveedor-agregar"),
    path('administracion/sucursales/crear/',login_required(views.SucursalCreateView.as_view()),name="administracion-sucursal-crear"),


    path('administracion/usuarios/',login_required(views.UserListView.as_view()),name="administracion_usuarios"),
    path('administracion/usuarios/crear/',login_required(views.UserCreateView.as_view()),name="administracion_usuarios_crear"),
    path('administracion/usuarios/actualizar/<slug:usr>',login_required(views.UserUpdateView.as_view()),name="administracion_usuarios_actualizar"),
    path('administracion/usuarios/pwd/<slug:usr>',login_required(views.UserPasswordUpdateView.as_view()),name="administracion_usuarios_actualizar_pwd"),
    path('administracion/usuarios/activar/<slug:usr>',login_required(views.UserDeactivateView.as_view()),name="administracion_usuarios_activar"),

    # [------------- INVENTARIOS --------------] # 
    path('inventarios/',login_required(views.InventariosView.as_view()),name="inventarios"),
    path('inventarios/agregar/',login_required(views.InventariosCreateView.as_view()),name="inventarios-agregar"),
    path('inventarios/traspaso/',login_required(views.TraspasoView.as_view()),name="administracion-traspaso"),

    # [------------- API --------------] # 
    path('api/',include(router.urls))
] 