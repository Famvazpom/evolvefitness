from django.db import models

# Create your models here.
class Equipo(models.Model):

    

    class Meta:
        verbose_name = ("Equipo")
        verbose_name_plural = ("Equipos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Equipo_detail", kwargs={"pk": self.pk})
