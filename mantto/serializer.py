from rest_framework import serializers
from django.urls import reverse_lazy
from .models import *



class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ("pk","nombre","css_class")

class GimnasioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gimnasio
        fields = ("__all__")
    

class ReporteSerializer(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    fecha = serializers.SerializerMethodField()
    asignado = serializers.SerializerMethodField()
    estado = EstadoSerializer()
    url = serializers.SerializerMethodField()
    ultima_modificacion = serializers.SerializerMethodField()
    class Meta:
        model = Reporte
        fields = ("pk","fecha","gym","asignado","estado",'falla','url','ultima_modificacion')

    def get_fecha(self,reporte):
        return reporte.fecha.date()

    def get_asignado(self,reporte):
        return reporte.asignado.__str__()
    
    def get_url(self,reporte):
        return reverse_lazy('reporte_detalles', kwargs={ 'id': reporte.pk})
    
    def get_ultima_modificacion(self,reporte):
        return f'{reporte.ultima_modificacion.date()}'
