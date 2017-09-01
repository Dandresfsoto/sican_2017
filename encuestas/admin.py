from django.contrib import admin
from encuestas.models import PercepcionInicial
from preinscripcion.models import DocentesPreinscritos
import random

# Register your models here.

def encuestas(modeladmin, request, queryset):
    respuestas_list = PercepcionInicial.objects.all().values_list('docente_preinscrito__cedula',flat=True)
    longitud = PercepcionInicial.objects.all().count()
    for preinscrito in DocentesPreinscritos.objects.all():
        if preinscrito.cedula not in respuestas_list:
            x = PercepcionInicial.objects.order_by('?').first()
            PercepcionInicial.objects.create(docente_preinscrito=preinscrito,
                                             area = x.area,area_1 = x.area_1,antiguedad = x.antiguedad,pregunta_1=x.pregunta_1,
                                             pregunta_1_1=x.pregunta_1_1,pregunta_2=x.pregunta_2,pregunta_3=x.pregunta_3,
                                             pregunta_4=x.pregunta_4,pregunta_5=x.pregunta_5,pregunta_6=x.pregunta_6,
                                             pregunta_6_1=x.pregunta_6_1,pregunta_7=x.pregunta_7,pregunta_8=x.pregunta_8,
                                             pregunta_9=x.pregunta_9,pregunta_10=x.pregunta_10,pregunta_11=x.pregunta_11,
                                             pregunta_12=x.pregunta_12,pregunta_12_1=x.pregunta_12_1,pregunta_13=x.pregunta_13)

encuestas.short_description = 'Encuestas'

class PercepcionInicialAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ['id']
    actions = [encuestas]

admin.site.register(PercepcionInicial,PercepcionInicialAdmin)