from mantto.models import FotoReporte
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Gimnasio)
admin.site.register(Equipo)
admin.site.register(Reporte)
admin.site.register(Perfil)
admin.site.register(Rol)
admin.site.register(Estado)
admin.site.register(FotoReporte)