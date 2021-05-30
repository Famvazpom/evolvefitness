from rest_framework import viewsets
from .models import *
from .serializer import *

class ReporteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reporte.objects.all().order_by('-ultima_modificacion')
    serializer_class = ReporteSerializer

    def get_queryset(self):
        out = self.queryset
        gym = self.request.query_params.get('gym')
        asignado = self.request.query_params.get('asignado')
        maquina = self.request.query_params.get('maquina')
        status = self.request.query_params.get('status')
        if gym is not None:
            out = out.filter(gym=gym)
        if maquina is not None:
            out = out.filter(equipo=maquina)
        if asignado is not None:
            out = out.filter(asignado=asignado)
        if status is not None:
            out = out.filter(estado=status)

        return out.filter(asignado=self.request.user.perfil) if self.request.user.perfil.rol == Rol.objects.get(nombre='Mantenimiento') else out