import os
from uuid import uuid4

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import User



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

eq_path = pathandrename('images/equipos/')
rep_path = pathandrenameReporte('images/reportes/')

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.nombre}'

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Perfil")
        verbose_name_plural = ("Perfiles")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

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


class Reporte(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    gym = models.ForeignKey(Gimnasio, on_delete=models.CASCADE)
    reporto = models.ForeignKey(Perfil, related_name=("Reporto"), on_delete=models.CASCADE)
    asignado = models.ForeignKey(Perfil,related_name=("Asignado"), on_delete=models.CASCADE)
    diagnostico = models.TextField(blank=True)
    falla = models.TextField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    costo = models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2)
    revisado = models.BooleanField(default=False)
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

    def __str__(self):
        return f'{self.reporte}'



@receiver(models.signals.post_delete, sender=FotoReporte)
@receiver(models.signals.post_delete, sender=FotosEquipo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)
