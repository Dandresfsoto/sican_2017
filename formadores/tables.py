#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_tables2 as tables
from formadores.models import SolicitudTransporte
from django.utils.safestring import mark_safe
import locale
from productos.models import Entregable
from formadores.models import Cortes
from formadores.models import Formador, Revision, Producto
import pytz
from cargos.models import Cargo

class SolicitudTable(tables.Table):
    nombre = tables.Column('Nombre')
    creacion_date = tables.Column('Fecha')
    valor = tables.Column('Valor solicitado')
    estado = tables.Column('Estado')
    terminada = tables.Column('Soporte')
    desplazamientos = tables.Column('Excel')
    observacion = tables.Column('Observación')
    valor_aprobado = tables.Column('Valor aprobado')


    def render_estado(self,value,record):
        if value == 'revision' or value == 'aprobado_lider':
            return mark_safe('<img src="/static/img/reloj.png" height="32" width="32">'
                             '<p>Esperando aprobación</p>')

        if value == 'aprobado' or value == 'consignado':
            if record.get_archivo_url() != '':
                if record.terminada:
                    return mark_safe('<img src="/static/img/true.png" height="32" width="32">'
                                 '<p>Consignado</p>')
                else:
                    return mark_safe('<img src="/static/img/esperando.png" height="32" width="32">'
                                 '<p>Esperando consignación</p>')
            else:
                return mark_safe('<img src="/static/img/alert.png" height="32" width="32">'
                                 '<p>Esperando firma de soporte</p>')

        if value == 'rechazado':
            return mark_safe('<img src="/static/img/delete.png" height="32" width="32">'
                             '<p>Solicitud rechazada</p>')


    def render_valor(self,value):
        return locale.currency(value,grouping=True)

    def render_desplazamientos(self,value,record):
        if record.estado == 'revision':
            return ''
        if record.estado == 'aprobado' or record.estado == 'consignado':
            return mark_safe('<a href="'+ record.get_pdf_url() +'"><img src="/static/img/file.png" height="32" width="32"><p>Descargar archivo</p></a>')
        if record.estado == 'rechazado':
            return ''
        else:
            return ''

    def render_terminada(self,value,record):
        if record.estado == 'revision':
            return ''
        if record.estado == 'aprobado' or record.estado == 'consignado':
            if record.get_archivo_url() == '':
                return mark_safe('<a href="soporte/'+ unicode(record.id) +'">Clic para subir soporte</a>')
            else:
                return mark_safe('<a target="_blank" href="'+ record.get_archivo_url() +'"><img src="/static/img/file.png" height="32" width="32"><p>Ver soporte</p></a>')
        if record.estado == 'rechazado':
            return ''
        else:
            return ''

    def render_valor_aprobado(self,value,record):
        if record.estado == 'revision' or record.estado == 'aprobado_lider':
            return ''
        if record.estado == 'aprobado' or record.estado == 'consignado':
            return locale.currency(value,grouping=True)
        if record.estado == 'rechazado':
            return ''


    class Meta:
        model = SolicitudTransporte
        fields = ['nombre','creacion_date','valor','estado','desplazamientos','terminada','observacion','valor_aprobado']


class TipologiasTable(tables.Table):
    nombre = tables.Column('Tipologia')



    def render_nombre(self,value,record):
        return mark_safe('<a href="cargo/'+ str(record.id) +'">' + record.nombre +'</a>')


    class Meta:
        model = Cargo
        fields = ['nombre']


class EntregablesTable(tables.Table):
    sesion = tables.Column('Sesión')
    nombre = tables.Column('Nombre')
    numero = tables.Column('Numero')
    tipo = tables.Column('Tipo')
    formato = tables.Column('Formato')



    def render_formato(self,value,record):
        if record.get_archivo_url() != '':
            return mark_safe('<a href="'+ record.get_archivo_url() +'"><img src="/static/img/file.png" height="32" width="32"></a>')
        else:
            return ''


    class Meta:
        model = Entregable
        fields = ['sesion','nombre','numero','tipo','formato']


class CortesTable(tables.Table):
    id_formador = None
    id = tables.Column('Corte')
    year = tables.Column('Año')
    descripcion = tables.Column('Valor reportado')

    def __init__(self, *args, **kwargs):
        temp = kwargs.pop("id_formador")
        super(CortesTable, self).__init__(*args, **kwargs)
        self.id_formador = temp

    def render_id(self,value,record):
        return mark_safe('<a href="'+ str(value) +'">COR-' + str(value) + '</a>')


    def render_descripcion(self,value,record):
        formador = Formador.objects.get(id=self.id_formador)
        corte = Cortes.objects.get(id = record.id)
        valor = 0
        for revision in Revision.objects.filter(formador_revision = formador, corte = corte):
            for producto in revision.productos.all():
                valor += producto.cantidad * producto.valor_entregable.valor
        return locale.currency( valor, grouping=True ).replace('+','')


    class Meta:
        model = Cortes
        fields = ['id','year','descripcion']


class RevisionTable(tables.Table):
    id = tables.Column('Código de pago')
    productos = tables.Column('Valor reportado')


    def render_id(self,value,record):
        return mark_safe('<a href="'+ str(value) +'">PAG-' + str(value) + '</a>')


    def render_productos(self,value,record):
        revision = Revision.objects.get(id = record.id)
        valor = 0
        for producto in revision.productos.all():
            valor += producto.cantidad * producto.valor_entregable.valor
        return locale.currency( valor, grouping=True ).replace('+','')


    class Meta:
        model = Revision
        fields = ['id','productos']


class PagoTable(tables.Table):
    nivel = tables.Column('Nivel', accessor= 'id', orderable=False)
    sesion = tables.Column('Sesion', accessor= 'id', orderable=False)
    id = tables.Column('Entregable')
    cantidad = tables.Column('Cantidad')
    valor_entregable = tables.Column('Valor individual')
    total = tables.Column('Valor total', accessor= 'id', orderable=False)

    def render_id(self,value,record):
        return record.valor_entregable.entregable.nombre


    def render_valor_entregable(self,value,record):
        return locale.currency( record.valor_entregable.valor, grouping=True ).replace('+','')

    def render_nivel(self,value,record):
        return record.valor_entregable.entregable.sesion.nivel.nombre

    def render_sesion(self,value,record):
        return record.valor_entregable.entregable.sesion.nombre

    def render_total(self,value,record):
        return locale.currency( record.valor_entregable.valor * record.cantidad, grouping=True ).replace('+','')

    class Meta:
        model = Producto
        fields = ['nivel','sesion','id','cantidad','valor_entregable','total']