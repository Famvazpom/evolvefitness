from mantto.serializer import FotoReporteSerializer
from django.db.models import Q
from rest_framework import viewsets,pagination
from .models import *
from .serializer import *

class EquipoPaginator(pagination.PageNumberPagination):       
       page_size = 300

class EquipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipo.objects.all().order_by('pk')
    serializer_class_normal = EquipoSerializer
    serializer_class = EquipoSerializerAdmin
    pagination_class = EquipoPaginator

    def get_serializer_class(self):
        if self.request.user.perfil.rol == Rol.objects.get(nombre="Administrador"):
            return self.serializer_class
        else:
            return self.serializer_class_normal

    def get_queryset(self):
        out = self.queryset
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
        out = self.queryset
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