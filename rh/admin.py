from django.contrib import admin
from rh.models import TipoSoporte, RequerimientoPersonal
from formadores.models import Soporte
# Register your models here.
admin.site.register(TipoSoporte)
admin.site.register(Soporte)
admin.site.register(RequerimientoPersonal)