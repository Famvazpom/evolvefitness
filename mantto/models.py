import os
from uuid import uuid4

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from pyheif_pillow_opener import register_heif_opener


register_heif_opener()

@deconstructible
class pathandrename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = filename.split('.')[:-1]
        # set filename as random string
        name = f'Equipo - {instance.equipo.pk} - { filename }'
        filename = '{}.{}'.format(name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

@deconstructible
class pathandrenameReporte(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = filename.split('.')[:-1]
        # set filename as random string
        name = f'Reporte - {instance.reporte.pk} { filename }'
        filename = '{}.{}'.format(name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

@deconstructible
class pathandrenameGasto(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = filename.split('.')[:-1]
        # set filename as random string
        name = f'Gasto - {instance.gasto.pk} { filename }'
        filename = '{}.{}'.format(name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

@deconstructible
class pathandrenameArchivo(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = filename.split('.')[:-1]
        # set filename as random string
        name = f'Gasto - {instance.pk} - { filename }'
        filename = '{}.{}'.format(name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

@deconstructible
class pathandrenameProducto(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def delete_file(self,instance):
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = filename.split('.')[:-1]
        # set filename as random string
        if not instance.pk:
            obj = Producto.objects.last()
            if obj:
                name = f'Producto - {obj.pk+1} - { filename }'
            else:
                name = f'Producto - {1} - { filename }'
        else:
            old = instance.__class__.objects.get(id=instance.id)
            if old.foto:
                self.delete_file(old)
            name = f'Producto - {instance.pk} - { filename }'
        filename = '{}.{}'.format(name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

eq_path = pathandrename('images/equipos/')
rep_path = pathandrenameReporte('images/reportes/')
repnota_path = pathandrenameGasto('images/notas_reportes/')
gasto_path = pathandrenameArchivo('files/gastos/')
producto_path = pathandrenameProducto('images/productos/')

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.nombre}'

class Gimnasio(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()

    class Meta:
        verbose_name_plural = "Gimnasios"

    def save(self,*args,**kwargs):
        self.nombre = self.nombre.upper()
        return super(Gimnasio,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.nombre)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gimnasio, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Perfil")
        verbose_name_plural = ("Perfiles")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

# Create your models here.
class Equipo(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField( max_length=100)
    marca = models.CharField( max_length=50)
    modelo = models.CharField( max_length=50)
    gym = models.ForeignKey(Gimnasio, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Equipo")
        verbose_name_plural = ("Equipos")

    def __str__(self):
        return f'{self.nombre} {self.marca} - Id: {self.id}'

    def save(self,*args,**kwargs):
        self.nombre = self.nombre.upper()
        self.marca = self.marca.upper()
        return super(Equipo,self).save(*args,**kwargs)

class FotosEquipo(models.Model):
    img = models.ImageField(upload_to=eq_path, height_field=None, width_field=None, max_length=None)
    equipo = models.ForeignKey(Equipo,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        
        if self.img:
            filename = "%s.jpg" % self.img.name.split('.')[0]
            
            img = Image.open(self.img).convert('RGB')
            # for PNG images discarding the alpha channel and fill it with some color
            if img.mode in ('RGBA', 'LA'):
                    background = Image.new(img.mode[:-1], img.size, '#fff')
                    background.paste(img, img.split()[-1])
                    img = background
            image_io = BytesIO()
            img.save(image_io, format='JPEG', quality=50)

            # change the img field value to be the newly modified img value
            self.img.save(filename, ContentFile(image_io.getvalue()), save=False)

        super(FotosEquipo, self).save(*args, **kwargs)

    def __str__(self):
        return f'Foto de {self.equipo}'

class Estado(models.Model):

    nombre = models.CharField( max_length=50)
    css_class = models.CharField( max_length=50)

    class Meta:
        verbose_name = ("Estado")
        verbose_name_plural = ("Estados")

    def __str__(self):
        return self.nombre

class TipoPagoReporte(models.Model):
    nombre = models.CharField( max_length=50)
    class Meta:
        verbose_name = ("Tipo de Pago")
        verbose_name_plural = ("Tipos de Pago")

    def __str__(self):
        return self.nombre

class ReporteMensaje(models.Model):
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Perfil,null=True,on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("Reporte Mensaje")
        verbose_name_plural = ("Reporte Mensajes")

    def __str__(self):
        return f'{ self.fecha.date() } - { self.mensaje }'

class Reporte(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    gym = models.ForeignKey(Gimnasio, on_delete=models.CASCADE)
    reporto = models.ForeignKey(Perfil, related_name=("Reporto"), on_delete=models.CASCADE)
    asignado = models.ManyToManyField(Perfil,related_name=("Personas_asignadas"))
    falla = models.TextField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    revisado = models.BooleanField(default=False)
    mensajes = models.ManyToManyField(ReporteMensaje)

    class Meta:
        verbose_name = ("Reporte")
        verbose_name_plural = ("Reportes")

    def __str__(self):
        return f'Reporte: {self.pk} - {self.equipo}'

class FotoReporte(models.Model):
    reporte = models.ForeignKey(Reporte, verbose_name=("Reporte Relacionado"), on_delete=models.CASCADE)
    img = models.ImageField(upload_to=rep_path, height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = ("Foto de Reporte")
        verbose_name_plural = ("Fotos de Reportes")

    def save(self, *args, **kwargs):
        
        if self.img:
            filename = "%s.jpg" % self.img.name.split('.')[0]
            
            img = Image.open(self.img).convert('RGB')
            # for PNG images discarding the alpha channel and fill it with some color
            if img.mode in ('RGBA', 'LA'):
                    background = Image.new(img.mode[:-1], img.size, '#fff')
                    background.paste(img, img.split()[-1])
                    img = background
            image_io = BytesIO()
            img.save(image_io, format='JPEG', quality=50)

            # change the img field value to be the newly modified img value
            self.img.save(filename, ContentFile(image_io.getvalue()), save=False)

        super(FotoReporte, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.reporte}'


class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10,blank=True,null=True,default='-')

    class Meta:
        verbose_name = ("Proveedor")
        verbose_name_plural = ("Proveedores")

    def __str__(self):
        return f'{self.nombre}'


class Gasto(models.Model):
    reportes = models.ManyToManyField(Reporte, verbose_name=("Reportes relacionados"),blank=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.ForeignKey(Perfil,blank=True,null=True,verbose_name=("Usuario que hizo el pago"), on_delete=models.CASCADE)
    pagado = models.BooleanField()
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor,blank=True,null=True,related_name=("Proveedor"),on_delete=models.CASCADE)
    gym = models.ForeignKey(Gimnasio,blank=True,null=True,on_delete=models.CASCADE)
    forma_pago = models.ForeignKey(TipoPagoReporte,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return f'Gasto: {self.pk} - ${ self.importe } - { self.gym }'

class GastosArchivos(models.Model):
    archivo = models.FileField(upload_to=gasto_path, max_length=100)
    gasto = models.ForeignKey(Gasto,on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Archivo de un Gasto")
        verbose_name_plural = ("Archivos de los Gastos")
    
    def __str__(self):
        return f'Gasto relacionado: {self.gasto.pk}'

class FotoNotaReporte(models.Model):
    gasto = models.ForeignKey(Gasto, verbose_name=("Reporte Relacionado"), on_delete=models.CASCADE)
    img = models.ImageField(upload_to=repnota_path, height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = ("Foto de Nota de Reporte")
        verbose_name_plural = ("Fotos de Notas de Reportes")

    def save(self, *args, **kwargs):
        
        if self.img:
            filename = "%s.jpg" % self.img.name.split('.')[0]
            
            img = Image.open(self.img).convert('RGB')
            # for PNG images discarding the alpha channel and fill it with some color
            if img.mode in ('RGBA', 'LA'):
                    background = Image.new(img.mode[:-1], img.size, '#fff')
                    background.paste(img, img.split()[-1])
                    img = background
            image_io = BytesIO()
            img.save(image_io, format='JPEG', quality=50)

            # change the img field value to be the newly modified img value
            self.img.save(filename, ContentFile(image_io.getvalue()), save=False)

        super(FotoNotaReporte, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk} - {self.gasto}'

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    presentacion = models.CharField(max_length=50)
    costo = models.FloatField()
    proveedor = models.ForeignKey(Proveedor,null = True,blank= True, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to=producto_path,blank=True,null=True)
    
    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def __str__(self):
        return f'{self.pk} - {self.nombre} - {self.presentacion}'

class Almacen(models.Model):
    gym = models.ForeignKey(Gimnasio,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.FloatField(verbose_name=("Precio de Venta"))
    existencias = models.PositiveIntegerField(default = 0)
    
    class Meta:
        verbose_name = ("Almacen")
        verbose_name_plural = ("Almacenes")

    def __str__(self):
        return f'{self.gym} - {self.producto} - ${self.precio}'



@receiver(models.signals.post_delete, sender=FotoReporte)
@receiver(models.signals.post_delete, sender=FotosEquipo)
@receiver(models.signals.post_delete, sender=FotoNotaReporte)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)

@receiver(models.signals.post_delete, sender=Producto)
def auto_delete_file_on_delete_files(sender, instance, **kwargs):
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)       

@receiver(models.signals.post_delete, sender=GastosArchivos)
def auto_delete_file_on_delete_files(sender, instance, **kwargs):
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)
