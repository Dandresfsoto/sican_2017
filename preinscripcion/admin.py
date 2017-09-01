from django.contrib import admin
from preinscripcion.models import DocentesPreinscritos
from matrices.models import Beneficiario
from preinscripcion.models import DocentesPreinscritos
from datetime import datetime

# Register your models here.

def preinscritos(modeladmin, request, queryset):
    preinscritos_list = DocentesPreinscritos.objects.all().values_list('cedula',flat=True)
    for beneficiario in Beneficiario.objects.exclude(radicado = None):
        if beneficiario.cedula not in preinscritos_list:
            cargo = 'Docente'
            if beneficiario.diplomado.numero == 3:
                cargo = 'Directivo Docente'
            DocentesPreinscritos.objects.create(cedula = beneficiario.cedula,primer_apellido=beneficiario.apellidos,
                                                primer_nombre=beneficiario.nombres,cargo=cargo,departamento=beneficiario.radicado.municipio.departamento,
                                                municipio=beneficiario.radicado.municipio,radicado=beneficiario.radicado,
                                                verificado=True,fecha=datetime.now().date(),masivo=True)
preinscritos.short_description = 'Copiar preinscritos'

class DocentesPreinscritosAdmin(admin.ModelAdmin):
    list_display = ['cedula','primer_nombre','primer_apellido']
    ordering = ['cedula']
    actions = [preinscritos]

admin.site.register(DocentesPreinscritos,DocentesPreinscritosAdmin)