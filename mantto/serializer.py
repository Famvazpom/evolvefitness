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
    equipo = EquipoSerializer()
    mensajes = ReporteMensajeSerializer(read_only=True,many=True)
    tipopago = TipoPagoSerializer(read_only=True)
    class Meta:
        model = Reporte
        fields = ("__all__")


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
    equipo = EquipoSerializer()
    mensajes = ReporteMensajeSerializer(read_only=True,many=True)
    tipopago = TipoPagoSerializer(read_only=True)
    class Meta:
        model = Reporte
        fields = ('__all__')

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

class GastoSerializer(serializers.ModelSerializer):
    pago = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    gym = serializers.SerializerMethodField()
    forma_pago = serializers.SerializerMethodField()
    proveedor = serializers.SerializerMethodField()
    importe = serializers.SerializerMethodField()
    detalles = serializers.SerializerMethodField()
    archivos =serializers.SerializerMethodField()
    pagado = serializers.BooleanField()
    reportes = serializers.SerializerMethodField()
    eliminar = serializers.SerializerMethodField()
    class Meta:
        model = Gasto
        fields = ('__all__')

    def get_pago(self,gasto):
        return gasto.pago.__str__() if gasto.pago else None

    def get_fecha(self,gasto):
        return gasto.fecha.date()
    
    def get_gym(self, obj):
        return obj.gym.__str__()
    
    def get_forma_pago(self, obj):
        return obj.forma_pago.__str__()

    def get_proveedor(self,obj):
        return obj.proveedor.__str__() if obj.proveedor else ""



    def get_importe(self, obj):
        return f'${obj.importe}' if obj.importe else "$-.--"

    def get_detalles(self,obj):
        url = reverse_lazy('administracion-gastos-actualizar',kwargs={'gasto':obj.pk})
        return f'<a class="btn btn-info btn-circle" onclick="openModal(\'{ url }\')" > <i class="fas fa-info-circle"></i>Detalles </a>'

    def get_archivos(self,obj):
        return '<a class="btn btn-info btn-circle" > <i class="fas fa-download"></i>Descargar </a>'

    def get_eliminar(self,obj):
        url = reverse_lazy('gastos-eliminar',kwargs={'id':obj.pk})
        return f'<a class="btn btn-danger btn-circle" onclick="openModal(\'{ url }\')" > <i class="fas fa-trash"></i>Eliminar </a>'
    
    def get_reportes(self,obj):
        end = ""
        for rep in obj.reportes.all():
            
            url = reverse_lazy('reporte_detalles', kwargs={ 'id': rep.pk})
            
            end+=f'<a onclick="openModal(\'{url}\')" class=" m-1 btn btn-info ">{rep.pk}</a>'
        return end

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ('__all__')

class ProductoSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    detalles = serializers.SerializerMethodField()
    eliminar = serializers.SerializerMethodField()
    proveedor = serializers.SerializerMethodField()
    costo = serializers.SerializerMethodField()
    
    def get_costo(self, obj):
        return f'${obj.costo}'
    
    def get_proveedor(self, obj):
        return obj.proveedor.__str__() if obj.proveedor else "Pendiente"
    
    def get_detalles(self, obj):
        return reverse_lazy('administracion-producto-modificar',kwargs = {'producto': obj.pk})

    def get_eliminar(self, obj):
        return reverse_lazy('administracion-producto-eliminar',kwargs = {'producto': obj.pk})
    
    def get_foto(self, obj):
        return obj.foto.url if obj.foto else None
        
    class Meta:
        model = Producto
        fields = ('__all__')


class AlmacenSerializer(serializers.ModelSerializer):
    gym = GimnasioSerializer()
    producto = ProductoSerializer()
    precio = serializers.SerializerMethodField()
    
    def get_precio(self, obj):
        return f'${ obj.precio }'
    

        
    class Meta:
        model = Almacen
        fields = ('__all__')



