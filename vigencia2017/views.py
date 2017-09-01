from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from vigencia2017.models import DaneSEDE, TipoContrato, ValorEntregableVigencia2017, CargaMatriz
from vigencia2017.forms import DaneSEDEForm, GruposForm, TipoContratoForm, ValorEntregableVigencia2017Form, CargaMatrizForm
from formadores.models import Contrato, Grupos
from productos.models import Entregable
from productos.models import Diplomado
from vigencia2017.tasks import carga_masiva_matrices
from vigencia2017.models import Grupos as GruposVigencia2017
from vigencia2017.models import Beneficiario as BeneficiarioVigencia2017
from vigencia2017.forms import BeneficiarioVigencia2017Form, NewBeneficiarioVigencia2017Form
from vigencia2017.models import Evidencia as EvidenciaVigencia2017
from vigencia2017.forms import EvidenciaVigencia2017Form, GruposVigencia2017ConectividadForm, MasivoVigencia2017Form
from vigencia2017.models import Evidencia, Red
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from vigencia2017.models import Pago as PagoVigencia2017
import shutil
from vigencia2017.models import CargaMasiva2017
from django.core.files.uploadedfile import SimpleUploadedFile
from zipfile import ZipFile
from vigencia2017.forms import RedForm
from region.models import Region
from django.shortcuts import HttpResponseRedirect
from vigencia2017.tasks import build_red


from vigencia2017.tasks import carga_masiva_evidencia

# Create your views here.
class ListadoCodigosDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/dane/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.informes')
        return super(ListadoCodigosDaneView, self).get_context_data(**kwargs)


class NuevoCodigoDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = DaneSEDE
    form_class = DaneSEDEForm
    success_url = '../'
    template_name = 'vigencia2017/dane/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.crear"


class UpdateCodigoDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = DaneSEDE
    form_class = DaneSEDEForm
    success_url = '../../'
    template_name = 'vigencia2017/dane/editar.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.editar"


    def get_context_data(self, **kwargs):
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        return super(UpdateCodigoDaneView, self).get_context_data(**kwargs)









class ListadoGruposFormacionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.informes')
        return super(ListadoGruposFormacionView, self).get_context_data(**kwargs)




class ListadoGruposFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_formador.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.informes')
        kwargs['id_contrato'] = self.kwargs['pk']
        return super(ListadoGruposFormadorView, self).get_context_data(**kwargs)


class NuevoGrupoFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = Grupos
    form_class = GruposForm
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.crear"


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        return super(NuevoGrupoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk']}










class ListadoValorContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/valor_contratos/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear')
        return super(ListadoValorContratosView, self).get_context_data(**kwargs)



class NuevoValorContratoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = TipoContrato
    form_class = TipoContratoForm
    success_url = '../'
    template_name = 'vigencia2017/valor_contratos/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear"



class ValorProductosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         FormView):

    form_class = ValorEntregableVigencia2017Form
    success_url = '../../../'
    template_name = 'vigencia2017/valor_contratos/valor_diplomado.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear"

    def get_context_data(self, **kwargs):
        kwargs['contrato'] = TipoContrato.objects.get(id = self.kwargs['id_contrato']).nombre
        kwargs['diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        return super(ValorProductosView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['id_contrato'],'id_diplomado':self.kwargs['id_diplomado']}

    def form_valid(self, form):

        entregables = Entregable.objects.filter(sesion__nivel__diplomado__id=self.kwargs['id_diplomado']).order_by('numero')
        tipo_contrato = TipoContrato.objects.get(id = self.kwargs['id_contrato'])

        for entregable in entregables:
            valor, created = ValorEntregableVigencia2017.objects.get_or_create(entregable = entregable,tipo_contrato = tipo_contrato)
            valor.valor = form.cleaned_data[str(entregable.id)]
            valor.save()

        return super(ValorProductosView, self).form_valid(form)



class ListadoCargaMatrizView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/cargar_matriz/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.crear')
        return super(ListadoCargaMatrizView, self).get_context_data(**kwargs)




class NuevaCargaMatrizView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = CargaMatriz
    form_class = CargaMatrizForm
    success_url = '../'
    template_name = 'vigencia2017/cargar_matriz/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.crear"

    def get_initial(self):
        return {'id_usuario':self.request.user.id}

    def form_valid(self, form):
        self.object = form.save()
        carga_masiva_matrices.delay(self.object.id,self.request.user.email)
        return super(NuevaCargaMatrizView, self).form_valid(form)



class ListadoInscritosGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_inscritos.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        return super(ListadoInscritosGrupoView, self).get_context_data(**kwargs)



class EditarBeneficiarioGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = BeneficiarioVigencia2017
    form_class = BeneficiarioVigencia2017Form
    pk_url_kwarg = 'id_beneficiario'
    success_url = '../../'
    template_name = 'vigencia2017/grupos_formacion/editar_beneficiario.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.editar"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['cedula'] = BeneficiarioVigencia2017.objects.get(id=self.kwargs['id_beneficiario']).cedula
        return super(EditarBeneficiarioGrupoView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo']}


class NuevoBeneficiarioGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = BeneficiarioVigencia2017
    form_class = NewBeneficiarioVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nuevo_beneficiario.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.editar"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        return super(NuevoBeneficiarioGrupoView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo']}





class ListadoCambioMatrizView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/cargar_matriz/lista_cambios.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.ver"


    def get_context_data(self, **kwargs):
        kwargs['id_matriz'] = self.kwargs['pk']
        return super(ListadoCambioMatrizView, self).get_context_data(**kwargs)




class ArbolDiplomadoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/arbol.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['diplomado'] = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo']).diplomado.nombre
        return super(ArbolDiplomadoView, self).get_context_data(**kwargs)





class ListaEvidenciasEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_evidencias.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['diplomado'] = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo']).diplomado.nombre
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear')
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(ListaEvidenciasEntregableView, self).get_context_data(**kwargs)






class NuevaEvidenciasEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = EvidenciaVigencia2017
    form_class = EvidenciaVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nueva_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(NuevaEvidenciasEntregableView, self).get_context_data(**kwargs)

    def form_valid(self, form):


        if 'archivo' in form.cleaned_data.keys():

            self.object = form.save()


        else:
            output = StringIO.StringIO()
            output.write(form.cleaned_data['link'])

            output.seek(0,2)
            file_data = InMemoryUploadedFile(output, 'file', 'link.txt', None, output.tell(), None)

            self.object = form.save(commit=False)
            self.object.archivo = file_data
            self.object.save()


        cargados = self.object.beneficiarios_cargados.all()
        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(contrato=contrato, entregable=entregable).filter(
                beneficiarios_cargados__id__in=cargados.values_list('id', flat=True)).distinct()

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)
                cargado.delete_pago_entregable(id_entregable=evidencia.entregable.id)


        for cargado in form.cleaned_data['beneficiarios_cargados']:
            self.object.beneficiarios_cargados.add(cargado)
            cargado.set_pago_entregable(id_entregable=self.object.entregable.id,evidencia_id=self.object.id)


        return super(NuevaEvidenciasEntregableView,self).form_valid(form)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo'],
                'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}







class MasivoEvidenciasEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         FormView):
    form_class = MasivoVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/masivo_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(MasivoEvidenciasEntregableView, self).get_context_data(**kwargs)


    def form_valid(self, form):

        carga = CargaMasiva2017.objects.create(archivo=form.cleaned_data['archivo'])

        #carga_masiva_evidencia.delay(carga.id,self.kwargs['pk'],self.kwargs['id_entregable'],self.request.user.id)


        user = self.request.user
        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])

        soportes = ZipFile(carga.archivo, 'r')

        for soporte_info in soportes.infolist():
            soporte = soporte_info.filename
            try:
                cedula = soporte.split('/')[-1].split('.')[-2]
            except:
                pass
            else:
                try:
                    beneficiario = BeneficiarioVigencia2017.objects.get(cedula=cedula)
                except:
                    pass
                else:
                    evidencias = EvidenciaVigencia2017.objects.filter(entregable=entregable, contrato=contrato)
                    if evidencias.filter(beneficiarios_validados=beneficiario).count() == 0:
                        if evidencias.filter(beneficiarios_cargados=beneficiario).count() > 0:
                            evidencias_cargadas = evidencias.filter(beneficiarios_cargados=beneficiario)

                            for evidencia_cargada in evidencias_cargadas:
                                evidencia_cargada.beneficiarios_cargados.remove(beneficiario)
                                beneficiario.delete_pago_entregable(id_entregable=entregable.id)

                        archivo = SimpleUploadedFile(name=soporte, content=soportes.read(soporte_info))
                        evidencia = EvidenciaVigencia2017.objects.create(usuario=user, archivo=archivo,
                                                                         entregable=entregable,
                                                                         contrato=contrato)
                        evidencia.beneficiarios_cargados.add(beneficiario)
                        beneficiario.set_pago_entregable(id_entregable=entregable.id, evidencia_id=evidencia.id)



        return super(MasivoEvidenciasEntregableView,self).form_valid(form)






class EditarEvidenciaEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = EvidenciaVigencia2017
    form_class = EvidenciaVigencia2017Form
    success_url = '../../'
    pk_url_kwarg = 'id_evidencia'
    template_name = 'vigencia2017/grupos_formacion/editar_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.editar"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['id_evidencia'] = self.kwargs['id_evidencia']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(EditarEvidenciaEntregableView, self).get_context_data(**kwargs)

    def form_valid(self, form):

        for cargado in self.object.beneficiarios_cargados.all():
            cargado.delete_pago_entregable(id_entregable = self.object.entregable.id)


        if 'archivo' in form.cleaned_data.keys():

            self.object = form.save()


        else:
            output = StringIO.StringIO()
            output.write(form.cleaned_data['link'])

            output.seek(0,2)
            file_data = InMemoryUploadedFile(output, 'file', 'link.txt', None, output.tell(), None)

            self.object = form.save(commit=False)
            self.object.archivo = file_data
            self.object.save()



        cargados = self.object.beneficiarios_cargados.all()

        for cargado in cargados:
            cargado.delete_pago_entregable(id_entregable = self.object.entregable.id)


        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(contrato=contrato, entregable=entregable).filter(
                beneficiarios_cargados__id__in=cargados.values_list('id', flat=True)).distinct()

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)
                cargado.delete_pago_entregable(id_entregable=evidencia.entregable.id)


        for cargado in form.cleaned_data['beneficiarios_cargados']:
            self.object.beneficiarios_cargados.add(cargado)
            cargado.set_pago_entregable(id_entregable=self.object.entregable.id, evidencia_id=self.object.id)

        return super(EditarEvidenciaEntregableView,self).form_valid(form)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo'],
                'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}









class DeleteEvidenciaEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         DeleteView):
    model = EvidenciaVigencia2017
    success_url = '../../'
    pk_url_kwarg = 'id_evidencia'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.eliminar"

    def get(self, request, *args, **kwargs):

        evidencia = Evidencia.objects.get(id = kwargs['id_evidencia'])

        for cargado in evidencia.beneficiarios_cargados.all():
            cargado.delete_pago_entregable(id_entregable = evidencia.entregable.id)
        return self.post(request, *args, **kwargs)




class ConectividadGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = GruposVigencia2017
    form_class = GruposVigencia2017ConectividadForm
    pk_url_kwarg = 'id_grupo'
    success_url = '../../'
    template_name = 'vigencia2017/grupos_formacion/no_conectividad.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        return super(ConectividadGrupoView, self).get_context_data(**kwargs)


    def form_valid(self, form):
        self.object = form.save()

        archivo = form.cleaned_data['archivo']

        if archivo == None or archivo == False:
            self.object.no_conectividad = False
        else:
            self.object.no_conectividad = True

        self.object.save()

        return super(ConectividadGrupoView , self).form_valid(form)





class EvidenciasListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/evidencias/codigos/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_codigos.ver"

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_codigos.informes')
        return super(EvidenciasListView,self).get_context_data(**kwargs)



class BeneficiarioEvidenciaCedulaList(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/evidencias/cedula/lista_beneficiarios.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cedula_beneficiario.ver"



class BeneficiarioEvidenciaCedulaProductoList(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/evidencias/cedula/lista_productos.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cedula_beneficiario.ver"


    def get_context_data(self, **kwargs):
        kwargs['id_beneficiario'] = self.kwargs['id_beneficiario']
        kwargs['nombre_beneficiario'] = BeneficiarioVigencia2017.objects.get(id = self.kwargs['id_beneficiario']).get_full_name()
        return super(BeneficiarioEvidenciaCedulaProductoList,self).get_context_data(**kwargs)





class RedsListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/red/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_reds.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_reds.crear')
        return super(RedsListView,self).get_context_data(**kwargs)





class NuevoRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Red
    form_class = RedForm
    success_url = '../'
    template_name = 'evidencias/red/nuevo.html'
    permission_required = "permisos_sican.evidencias.red.crear"

    def get_context_data(self, **kwargs):

        evidencias = Evidencia.objects.filter(red_id = None)

        region_1 = Region.objects.get(numero = 1)
        region_2 = Region.objects.get(numero = 2)

        evidencias_r1 = evidencias.filter(contrato__formador__region = region_1)
        evidencias_r2 = evidencias.filter(contrato__formador__region = region_2)

        evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')

        evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')


        kwargs['formadores_innovatic_r1'] = evidencias_r1_innovatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r1'] = evidencias_r1_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r1'] = evidencias_r1_innovatic.count()

        kwargs['formadores_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r1'] = evidencias_r1_tecnotic.count()

        kwargs['formadores_directic_r1'] = evidencias_r1_directic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r1'] = evidencias_r1_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r1'] = evidencias_r1_directic.count()

        kwargs['formadores_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r1'] = evidencias_r1_escuelatic.count()

        kwargs['formadores_innovatic_r2'] = evidencias_r2_innovatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r2'] = evidencias_r2_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r2'] = evidencias_r2_innovatic.count()

        kwargs['formadores_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r2'] = evidencias_r2_tecnotic.count()

        kwargs['formadores_directic_r2'] = evidencias_r2_directic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r2'] = evidencias_r2_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r2'] = evidencias_r2_directic.count()

        kwargs['formadores_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r2'] = evidencias_r2_escuelatic.count()

        return super(NuevoRedView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        red = Red.objects.get(id = self.object.id)

        if not red.producto_final:
            evidencias = EvidenciaVigencia2017.objects.filter(red_id = None)

            region_1 = Region.objects.get(numero = 1)
            region_2 = Region.objects.get(numero = 2)

            evidencias_r1 = evidencias.filter(contrato__formador__region = region_1)
            evidencias_r2 = evidencias.filter(contrato__formador__region = region_2)

            evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
            evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
            evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
            evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')

            evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
            evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
            evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
            evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')



            if self.object.region.numero == 1:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    evidencias_r1_innovatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'TECNOTIC':
                    evidencias_r1_tecnotic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DIRECTIC':
                    evidencias_r1_directic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                    evidencias_r1_escuelatic.update(red_id = red.id)
                else:
                    pass

            elif self.object.region.numero == 2:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    evidencias_r2_innovatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'TECNOTIC':
                    evidencias_r2_tecnotic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DIRECTIC':
                    evidencias_r2_directic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                    evidencias_r2_escuelatic.update(red_id = red.id)
                else:
                    pass


            else:
                pass
            red.save()
            build_red.delay(red.id)
        else:

            pass
        return HttpResponseRedirect(self.get_success_url())