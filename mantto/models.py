import os
from uuid import uuid4

from django.db import models
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import User


@deconstructible
class pathandrename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        if instance.pk:
            try:
                ob = Equipo.objects.get(pk=instance.pk)
                os.remove(ob.imagen.path)
            except OSError:
                pass
            name = f'{instance.pk} - {instance.nombre} {instance.marca}'
            filename = '{}.{}'.format(name, ext)
        else:
            # set filename as random string
            try:
                last = Equipo.objects.latest('id')
                pk = last.pk
            except Equipo.DoesNotExist:
                pk = 0
            name = f'{pk+1} - {instance.nombre} {instance.marca}'
            filename = '{}.{}'.format(name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)
eq_path = pathandrename('images/equipos/')

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

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Marca"

    def save(self,*args,**kwargs):
        self.nombre = self.nombre.upper()
        return super(Marca,self).save(*args,**kwargs)

    def __str__(self):
        return self.nombre

# Create your models here.
class Equipo(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField( max_length=50)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.CharField( max_length=50)
    gym = models.ForeignKey(Gimnasio, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=eq_path, height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = ("Equipo")
        verbose_name_plural = ("Equipos")

    def __str__(self):
        return f'{self.nombre} {self.marca} - Id: {self.id}'

    def save(self,*args,**kwargs):
        self.nombre = self.nombre.upper()

        return super(Equipo,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("Equipo_detail", kwargs={"pk": self.pk})

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
    falla = models.TextField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    costo = models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2)
    class Meta:
        verbose_name = ("Reporte")
        verbose_name_plural = ("Reportes")

    def __str__(self):
        return f'Reporte: {self.pk} - {self.equipo}'
