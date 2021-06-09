from rest_framework import serializers
from django.urls import reverse_lazy
from django.utils.formats import number_format
from .models import *



class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ("pk","nombre","css_class")

class FotoReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoReporte
        fields = ("__all__")

class GimnasioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gimnasio
        fields = ("__all__")
    

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ("__all__")

class ReporteMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteMensaje
        fields = ("__all__")

class ReporteSerializer(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    fecha = serializers.SerializerMethodField()
    asignado = serializers.SerializerMethodField()
    estado = EstadoSerializer()
    url = serializers.SerializerMethodField()
    foto = serializers.SerializerMethodField()
    foto_url = serializers.SerializerMethodField()
    ultima_modificacion = serializers.SerializerMethodField()
    costo = serializers.SerializerMethodField('costo_localize')
    equipo = EquipoSerializer()
    mensajes = ReporteMensajeSerializer(read_only=True,many=True)
    class Meta:
        model = Reporte
        fields = ("pk","fecha","equipo","gym","mensajes","asignado","estado",'falla','foto','foto_url','url','costo','ultima_modificacion','revisado')

    def costo_localize(self,reporte):
        return number_format(reporte.costo) if reporte.costo else None

    def get_fecha(self,reporte):
        return reporte.fecha.date()

    def get_asignado(self,reporte):
        return reporte.asignado.__str__()
    
    def get_url(self,reporte):
        return reverse_lazy('reporte_detalles', kwargs={ 'id': reporte.pk})
    
    def get_foto_url(self,reporte):
        return reverse_lazy('reporte_fotos', kwargs={ 'id': reporte.pk})
    
    def get_foto(self,reporte):
        return True if FotoReporte.objects.filter(reporte=reporte.pk).count() > 0 else False
        return reverse_lazy('reporte_fotos', kwargs={ 'id': reporte.pk})
    
    def get_ultima_modificacion(self,reporte):
        return f'{reporte.ultima_modificacion.date()}'
