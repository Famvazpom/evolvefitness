from rest_framework import viewsets
from .models import *
from .serializer import *

class ReporteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reporte.objects.all().order_by('-ultima_modificacion')
    serializer_class = ReporteSerializer