from django.urls.base import reverse
from rest_framework import serializers
from django.urls import reverse_lazy
from django.utils.formats import number_format
from rest_framework.fields import SerializerMethodField
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
    

class EquipoSerializerAdmin(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    reportar = serializers.SerializerMethodField()
    modificar = serializers.SerializerMethodField()
    
    def get_modificar(self, obj):
        modify_url = reverse_lazy('equipo_actualizar',kwargs={ 'id_equipo': obj.pk })
        return f'<a onclick=\'openModal("{ modify_url }")\' class="btn btn-info">Modificar</a>'
        
    
    def get_reportar(self, obj):
        modify_url = reverse_lazy('reporte_crear',kwargs={ 'id_equipo': obj.pk })
        return f'<a onclick=\'openModal("{ modify_url }")\' class="btn btn-info">Reportar</a>'
        
    class Meta:
        model = Equipo
        fields = ("__all__")

class EquipoSerializer(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    reportar = serializers.SerializerMethodField()
    
    def get_reportar(self, obj):
        modify_url = reverse_lazy('reporte_crear',kwargs={ 'id_equipo': obj.pk })
        return f'<a onclick=\'openModal("{ modify_url }")\' class="btn btn-info">Reportar</a>'
        
    class Meta:
        model = Equipo
        fields = ("__all__")

class ReporteMensajeSerializer(serializers.ModelSerializer):
    fecha = serializers.SerializerMethodField()
    autor = serializers.SerializerMethodField()

    class Meta:
        model = ReporteMensaje
        fields = ("__all__")
    
    def get_fecha(self,reporte):
        return reporte.fecha.date()
    
    def get_autor(self,reporte):
        return reporte.autor.__str__() if reporte.autor else None
    

class TipoPagoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoPagoReporte
        fields = ("__all__")

class ReporteSerializer(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    fecha = serializers.SerializerMethodField()
    asignado = serializers.SerializerMethodField()
    reporto = serializers.SerializerMethodField()
    estado = EstadoSerializer()
    url = serializers.SerializerMethodField()
    foto = serializers.SerializerMethodField()
    foto_url = serializers.SerializerMethodField()
    ultima_modificacion = serializers.SerializerMethodField()
    costo = serializers.SerializerMethodField('costo_localize')
    equipo = EquipoSerializer()
    mensajes = ReporteMensajeSerializer(read_only=True,many=True)
    tipopago = TipoPagoSerializer(read_only=True)
    class Meta:
        model = Reporte
        fields = ("pk","fecha",'reporto','tipopago',"equipo","gym","mensajes","asignado","estado",'falla','foto','foto_url','url','costo','ultima_modificacion','revisado')

    def costo_localize(self,reporte):
        return number_format(reporte.costo) if reporte.costo else None

    def get_fecha(self,reporte):
        return reporte.fecha.date()

    def get_asignado(self,reporte):
        return [i.__str__() for i in reporte.asignado.all() ]
    
    def get_reporto(self,reporte):
        return reporte.reporto.__str__()
    
    def get_url(self,reporte):
        return reverse_lazy('reporte_detalles', kwargs={ 'id': reporte.pk})
    
    def get_foto_url(self,reporte):
        return reverse_lazy('reporte_fotos', kwargs={ 'id': reporte.pk})
    
    def get_foto(self,reporte):
        return True if FotoReporte.objects.filter(reporte=reporte.pk).count() > 0 else False
    
    def get_ultima_modificacion(self,reporte):
        return f'{reporte.ultima_modificacion.date()}'

class ReporteSerializerAdmin(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    fecha = serializers.SerializerMethodField()
    asignado = serializers.SerializerMethodField()
    reporto = serializers.SerializerMethodField()
    estado = EstadoSerializer()
    url = serializers.SerializerMethodField()
    foto = serializers.SerializerMethodField()
    foto_url = serializers.SerializerMethodField()
    ultima_modificacion = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()
    costo = serializers.SerializerMethodField('costo_localize')
    equipo = EquipoSerializer()
    mensajes = ReporteMensajeSerializer(read_only=True,many=True)
    tipopago = TipoPagoSerializer(read_only=True)
    class Meta:
        model = Reporte
        fields = ("pk","fecha",'delete','reporto','tipopago',"equipo","gym","mensajes","asignado","estado",'falla','foto','foto_url','url','costo','ultima_modificacion','revisado')

    def costo_localize(self,reporte):
        return number_format(reporte.costo) if reporte.costo else None

    def get_fecha(self,reporte):
        return reporte.fecha.date()

    def get_asignado(self,reporte):
        return [i.__str__() for i in reporte.asignado.all() ]
    
    def get_reporto(self,reporte):
        return reporte.reporto.__str__()
    
    def get_url(self,reporte):
        return reverse_lazy('reporte_detalles', kwargs={ 'id': reporte.pk})
    
    def get_foto_url(self,reporte):
        return reverse_lazy('reporte_fotos', kwargs={ 'id': reporte.pk})

    def get_delete(self,reporte):
        return reverse_lazy('reporte_eliminar', kwargs={ 'id': reporte.pk})
    
    def get_foto(self,reporte):
        return True if FotoReporte.objects.filter(reporte=reporte.pk).count() > 0 else False
    
    def get_ultima_modificacion(self,reporte):
        return f'{reporte.ultima_modificacion.date()}'
