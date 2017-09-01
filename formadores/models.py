from __future__ import unicode_literals

from django.db import models
from rh.models import TipoSoporte
from region.models import Region
from cargos.models import Cargo
from bancos.models import Banco
from departamentos.models import Departamento
from municipios.models import Municipio
import os
from usuarios.models import User
from productos.models import Contratos
from productos.models import ValorEntregable
from django.utils import timezone
from rh.models import TipoSoporte


class Formador(models.Model):

    usuario = models.ForeignKey(User,blank=True,null=True,related_name='usuario_sistema_formador')

    lider = models.ForeignKey(User,blank=True,null=True)
    departamentos = models.ManyToManyField(Departamento,related_name="departamento_formador",blank=True)
    codigo_ruta = models.CharField(max_length=100,blank=True,null=True)
    #---------- REGION----------------------
    region = models.ManyToManyField(Region)

    #---------- DATOS PERSONALES----------------------
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.BigIntegerField(unique=True)
    expedicion = models.CharField(max_length=100,blank=True)
    correo_personal = models.EmailField(max_length=100,blank=True)
    celular_personal = models.CharField(max_length=100,blank=True)


    #---------- INFORMACION PROFESIONAL ----------------------
    cargo = models.ManyToManyField(Cargo)
    respaldo_cargo = models.ForeignKey(Cargo,related_name="respaldo_cargo",blank=True,null=True)
    profesion = models.CharField(max_length=100,blank=True)

    fecha_contratacion = models.DateField(null=True,blank=True)
    fecha_terminacion = models.DateField(null=True,blank=True)

    #---------- INFORMACION BANCARIA Y SEGURIDAD SOCIAL ----------------------
    banco = models.ForeignKey(Banco,blank=True,null=True)
    tipo_cuenta = models.CharField(max_length=100,blank=True)
    numero_cuenta = models.CharField(max_length=100,blank=True)

    eps = models.CharField(max_length=100,blank=True)
    pension = models.CharField(max_length=100,blank=True)
    arl = models.CharField(max_length=100,blank=True)

    cantidad_docentes = models.IntegerField(default=150)
    primera_capacitacion = models.BooleanField(default=False)

    usuario_colombia_aprende = models.CharField(max_length=100,blank=True)
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombres']

    def __unicode__(self):
        return self.nombres + " " + self.apellidos

    def get_region_string(self):
        value = ''
        for region in self.region.values_list('nombre',flat=True):
            value = value + unicode(region) + ', '
        return value[:-2]

    def get_cargo_string(self):
        value = ''
        for cargo in self.cargo.values_list('nombre',flat=True):
            value = value + unicode(cargo) + ', '
        return value[:-2]

    def get_interventoria_region(self):
        value = ''
        for region in self.region.values_list('numero',flat=True):
            value = value + "R" + unicode(region) + ', '
        return value[:-2]

    def get_departamentos_string(self):
        value = ''
        for departamento in self.departamentos.values_list('nombre',flat=True):
            value = value + unicode(departamento) + ', '
        return value[:-2]


    def get_full_name(self):
        return self.nombres + " " + self.apellidos

class SolicitudSoportes(models.Model):
    nombre = models.CharField(max_length=200)
    soportes_requeridos = models.ManyToManyField(TipoSoporte)

    def __unicode__(self):
        return self.nombre

class Contrato(models.Model):
    nombre = models.CharField(unique=True,max_length=200)
    formador = models.ForeignKey(Formador)
    soportes_requeridos = models.ForeignKey(SolicitudSoportes)
    codigo_ruta = models.CharField(max_length=100,blank=True,null=True)
    vigencia = models.CharField(max_length=100,blank=True,null=True)
    fecha = models.DateTimeField(auto_now_add = True)
    fecha_inicio = models.DateField(blank=True,null=True)
    fecha_fin = models.DateField(blank=True,null=True)
    renuncia = models.BooleanField(default=False)
    soporte_renuncia = models.FileField(upload_to='Contratos/Formadores/Soporte Renuncia/',blank=True,null=True)
    liquidado = models.BooleanField(default=False)
    soporte_liquidacion = models.FileField(upload_to='Contratos/Formadores/Soporte Liquidacion/',blank=True,null=True)
    contrato_original = models.FileField(upload_to='Contratos/Formadores/Contrato Original/',blank=True,null=True)
    contrato_firmado = models.FileField(upload_to='Contratos/Formadores/Contrato Firmado/',blank=True,null=True)
    municipios = models.ManyToManyField(Municipio)
    supervisores = models.ManyToManyField(User)
    meta_beneficiarios = models.BigIntegerField()
    tipo_contrato_id = models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return self.nombre

    def get_contrato_url(self):
        try:
            url = self.contrato_original.url
        except:
            url = None
        return url

    def get_municipios_string(self):
        municipios = ''
        for municipio in self.municipios.all():
            municipios += municipio.__unicode__() + '</br>'
        return municipios

    def get_municipios_list(self):
        municipios = ''
        for municipio in self.municipios.all():
            municipios += municipio.nombre+','+municipio.departamento.nombre + ';'
        return municipios

    def get_supervisores_string(self):
        supervisores = ''
        for supervisor in self.supervisores.all():
            supervisores += supervisor.get_full_name_string()+ ' - '+ supervisor.email + '</br>'
        return supervisores

    def get_supervisores_list(self):
        supervisores = ''
        for supervisor in self.supervisores.all():
            supervisores += supervisor.get_full_name_string()+ ' - '+ supervisor.email + ';'
        return supervisores

class Soporte(models.Model):
    formador = models.ForeignKey(Formador)
    creacion = models.DateField(auto_now=True)
    fecha = models.DateField(blank=True,null=True)
    tipo = models.ForeignKey(TipoSoporte,related_name='soporte_formador')
    descripcion = models.TextField(max_length=1000,blank=True)
    oculto = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Formadores/Soportes/',blank=True)
    contrato = models.ForeignKey(Contrato,blank=True,null=True)

    class Meta:
        ordering = ['formador']

    def __unicode__(self):
        return str(self.formador.cedula)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)

class Desplazamiento(models.Model):
    departamento_origen = models.ForeignKey(Departamento,related_name="departamento_origen_desplazamiento")
    municipio_origen = models.ForeignKey(Municipio,related_name="municipio_origen_desplazamiento")
    departamento_destino = models.ForeignKey(Departamento,related_name="departamento_destino_desplazamiento")
    municipio_destino = models.ForeignKey(Municipio,related_name="municipio_destino_desplazamiento")
    valor = models.BigIntegerField()
    creacion = models.DateTimeField(auto_now=True)
    fecha = models.DateField()
    motivo = models.CharField(max_length=600)

    def __unicode__(self):
        return unicode(self.id)

class SolicitudTransporte(models.Model):
    formador = models.ForeignKey(Formador,related_name="formador_solicitud_transporte")
    nombre = models.CharField(max_length=100)
    creacion = models.DateTimeField(auto_now_add=True)
    creacion_date = models.DateTimeField(blank=True,null=True)
    aprobacion_lider = models.DateTimeField(blank=True,null=True)
    desplazamientos = models.ManyToManyField(Desplazamiento,blank=True)
    estado = models.CharField(max_length=100,default="revision")
    observacion = models.TextField(max_length=1000,blank=True,null=True)
    valor = models.BigIntegerField()
    terminada = models.BooleanField(default=False)
    valor_aprobado = models.BigIntegerField(blank=True,null=True)
    valor_aprobado_lider = models.BigIntegerField(blank=True,null=True)
    archivo = models.FileField(upload_to='Transportes/Solicitudes/',blank=True,null=True)
    pdf = models.FileField(upload_to = 'Transportes/Pdf/',blank=True,null=True)


    def __unicode__(self):
        return unicode(self.formador.cedula)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url

    def get_pdf_url(self):
        try:
            url = self.pdf.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)

class Grupos(models.Model):
    usuario = models.ForeignKey(User,blank=True,null=True)
    formador = models.ForeignKey(Formador,related_name="formador_grupos")
    nombre = models.CharField(max_length=100)
    oculto = models.BooleanField(default=False)
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return str(self.formador.codigo_ruta) + "-" + self.nombre

    def get_full_name(self):
        return self.formador.codigo_ruta + '-' + self.nombre

class Producto(models.Model):
    valor_entregable = models.ForeignKey(ValorEntregable)
    cantidad = models.IntegerField(null=True)

    def total(self):
        return self.valor_entregable * self.cantidad

class Cortes(models.Model):
    descripcion = models.TextField(max_length=500)
    fecha = models.DateTimeField(auto_now=True)
    archivo = models.FileField(upload_to='Cortes',blank=True,null=True)
    year = models.IntegerField(blank=True,null=True)
    mes = models.CharField(max_length=100,blank=True,null=True)

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url

class Revision(models.Model):
    formador_revision = models.ForeignKey(Formador)
    fecha = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(max_length=500,blank=True)
    productos = models.ManyToManyField(Producto,blank=True)
    corte = models.ForeignKey(Cortes,blank=True,null=True)


class CohortesFormadores(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='Cohortes/Formadores/Archivo/')
    resultado = models.FileField(upload_to='Cohortes/Formadores/Resultado/')
    contratos = models.FileField(upload_to='Cohortes/Formadores/Contratos/')

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url

    def get_resultado_url(self):
        try:
            url = self.resultado.url
        except:
            url = ""
        return url

    def get_contratos_url(self):
        try:
            url = self.contratos.url
        except:
            url = ""
        return url