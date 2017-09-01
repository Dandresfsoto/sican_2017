from django.contrib import admin
from evidencias.models import Evidencia, Red, CargaMasiva, Rechazo
from evidencias.tasks import carga_masiva_evidencias
# Register your models here.

admin.site.register(Evidencia)
admin.site.register(Red)

def masivo(modeladmin, request, queryset):
    for obj in queryset:
        carga_masiva_evidencias.delay(obj.id,request.user.id)
masivo.short_description = 'Ejecutar carga masiva'

class CargaMasivaAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ['id']
    actions = [masivo]

admin.site.register(CargaMasiva,CargaMasivaAdmin)
admin.site.register(Rechazo)