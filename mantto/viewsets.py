from mantto.serializer import FotoReporteSerializer
from django.db.models import Q
from rest_framework import viewsets,pagination
from .models import *
from .serializer import *


class EquipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipo.objects.all().order_by('pk')
    serializer_class_normal = EquipoSerializer
    serializer_class = EquipoSerializerAdmin
    pagination_class= None

    def get_serializer_class(self):
        if self.request.user.perfil.rol == Rol.objects.get(nombre="Administrador"):
            return self.serializer_class
        else:
            return self.serializer_class_normal

    def get_queryset(self):
        out = Equipo.objects.all().order_by('pk')
        gym = self.request.query_params.get('gym')
        maquina = self.request.query_params.get('maquina')
        idmaquina = self.request.query_params.get('id-maquina')
        marca = self.request.query_params.get('marca')

        if gym is not None:
            out = out.filter(gym=gym)
        
        if maquina is not None:
            out = out.filter(nombre__icontains=maquina)
        
        if idmaquina is not None:
            out = out.filter(pk=idmaquina)
        
        if marca is not None:
            out = out.filter(marca__icontains=marca)

        return out
    

class ReporteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reporte.objects.all().order_by('-ultima_modificacion')
    serializer_class = ReporteSerializerAdmin
    serializer_class_normal = ReporteSerializer

    def get_serializer_class(self):
        if self.request.user.perfil.rol == Rol.objects.get(nombre="Administrador"):
            return self.serializer_class
        else:
            return self.serializer_class_normal

    def get_queryset(self):
        out = Reporte.objects.all().order_by('-ultima_modificacion')
        gym = self.request.query_params.get('gym')
        asignado = self.request.query_params.get('asignado')
        maquina = self.request.query_params.get('maquina')
        status = self.request.query_params.get('status')
        revisado = self.request.query_params.get('revisado')
        if gym is not None:
            out = out.filter(gym=gym)
        if maquina is not None:
            if maquina.isnumeric():
                out = out.filter(equipo=maquina)
            else:
                out = out.filter(equipo__nombre__icontains=maquina)
            
        if asignado is not None:
            out = out.filter(asignado=asignado)
        if status is not None:
            out = out.filter(estado=status)
        if revisado:
            if revisado =='1':
                out = out.filter(revisado=True)
            if revisado == '2':
                out = out.filter(revisado=False)

        return out.filter(Q(asignado=self.request.user.perfil) | Q(reporto=self.request.user.perfil)) if self.request.user.perfil.rol == Rol.objects.get(nombre='Mantenimiento') else out
    
class FotoReporteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FotoReporte.objects.all()
    serializer_class = FotoReporteSerializer

    def get_queryset(self):
        out = self.queryset
        reporte = self.request.query_params.get('reporte')
        if reporte is not None:
            out = out.filter(reporte=reporte)

        return out

class GastoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gasto.objects.all().order_by('-fecha')
    serializer_class = GastoSerializer
    pagination_class = None

    def extra_filter_queryset(self):
        perfil = self.request.user.perfil
        queryset = Gasto.objects.all().order_by('-fecha')
        if perfil.rol == Rol.objects.get(nombre='Contabilidad'):
            return queryset.filter(Q(pago = perfil) | Q(forma_pago=TipoPagoReporte.objects.get(nombre='Transferencia')))
        if perfil.rol == Rol.objects.get(nombre = 'Recepcionista'):
            return queryset.filter(pago=perfil)
        return queryset
    
    def get_queryset(self):
        return self.extra_filter_queryset()


class ProveedorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    pagination_class = None

    def get_queryset(self):
        out = Producto.objects.all().order_by('nombre')
        nombre = self.request.query_params.get('nombre')
        if nombre:
            out = out.filter(nombre__icontains=nombre)
        return out
    

class AlmacenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    pagination_class = None


    def get_queryset(self):
        out = Almacen.objects.all()
        gym = self.request.query_params.get('gym')
        nombre = self.request.query_params.get('nombre')
        marca = self.request.query_params.get('marca')
        presentacion = self.request.query_params.get('presentacion')
        if gym:
            out = out.filter(gym__pk=gym)
        if nombre:
            out = out.filter(producto__nombre__icontains=nombre)
        if marca:
            out = out.filter(producto__marca__icontains=marca)
        if presentacion:
            out = out.filter(producto__presentacion__icontains=presentacion)
        return out

