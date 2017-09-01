from django.views.generic import FormView, CreateView, UpdateView, TemplateView
from django.shortcuts import HttpResponseRedirect
from docentes.models import DocentesDocentic, DocentesMinEducacion
from preinscripcion.models import DocentesPreinscritos
from encuestas.forms import Consulta, PercepcionInicialForm,PercepcionFinalForm
from encuestas.models import PercepcionInicial, PercepcionFinal
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class InicioView(FormView):
    template_name = 'encuestas/percepcion/consulta.html'
    form_class = Consulta
    success_url = '/preinscripcion/completo/'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        docentic = DocentesDocentic.objects.filter(cedula=cedula)
        mineducacion = DocentesMinEducacion.objects.filter(cedula=cedula)
        preinscritos = DocentesPreinscritos.objects.filter(cedula=cedula)

        redirect = '/preinscripcion/'

        if docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 1:
            redirect = '/preinscripcion/registro/'+str(cedula)

        elif docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 0:
            redirect = '/preinscripcion/preregistro/'+str(cedula)

        elif docentic.count() == 1:
            if docentic[0].informatica or docentic[0].directivo:
                redirect = '/preinscripcion/diploma_reingreso/'+str(cedula)
            else:
                redirect = '/preinscripcion/diploma/'+str(cedula)

        elif preinscritos.count() == 1:
            redirect = '/encuestas/percepcioninicial/'+str(cedula)

        return HttpResponseRedirect(redirect)

class EncuestaView(FormView):
    form_class = PercepcionInicialForm
    success_url = 'completo/'
    template_name = 'encuestas/percepcion/nuevo.html'

    def form_valid(self, form):

        nuevo = PercepcionInicial()
        nuevo.docente_preinscrito = DocentesPreinscritos.objects.get(cedula = self.kwargs['pk'])
        nuevo.area = form.cleaned_data['area']
        nuevo.area_1 = form.cleaned_data['area_1']
        nuevo.antiguedad = form.cleaned_data['antiguedad']
        nuevo.pregunta_1 = form.cleaned_data['pregunta_1']
        nuevo.pregunta_1_1 = form.cleaned_data['pregunta_1_1']
        nuevo.pregunta_2 = form.cleaned_data['pregunta_2']
        nuevo.pregunta_3 = form.cleaned_data['pregunta_3']
        nuevo.pregunta_4 = form.cleaned_data['pregunta_4']
        nuevo.pregunta_5 = form.cleaned_data['pregunta_5']
        nuevo.pregunta_6 = form.cleaned_data['pregunta_6']
        nuevo.pregunta_6_1 = form.cleaned_data['pregunta_6_1']
        nuevo.pregunta_7 = form.cleaned_data['pregunta_7']
        nuevo.pregunta_8 = form.cleaned_data['pregunta_8']
        nuevo.pregunta_9 = form.cleaned_data['pregunta_9']
        nuevo.pregunta_10 = form.cleaned_data['pregunta_10']
        nuevo.pregunta_11 = form.cleaned_data['pregunta_11']
        nuevo.pregunta_12 = form.cleaned_data['pregunta_12']
        nuevo.pregunta_12_1 = form.cleaned_data['pregunta_12_1']
        nuevo.pregunta_13 = form.cleaned_data['pregunta_13']
        nuevo.save()

        return HttpResponseRedirect(self.get_success_url())

class CompletoView(TemplateView):
    template_name = 'encuestas/percepcion/completo.html'


class ResultadosPercepcionInicialView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'encuestas/percepcion/resultados.html'
    permission_required = "permisos_sican.encuestas.percepcioninicial.ver"


class RespuestasPercepcionInicialView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'encuestas/resultados_percepcion/lista.html'
    permission_required = "permisos_sican.encuestas.respuestaspercepcioninicial.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.encuestas.respuestaspercepcioninicia.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.encuestas.respuestaspercepcioninicia.informes')
        return super(RespuestasPercepcionInicialView, self).get_context_data(**kwargs)


class FinalView(FormView):
    template_name = 'encuestas/percepcionfinal/consulta.html'
    form_class = Consulta
    success_url = '/preinscripcion/completo/'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        docentic = DocentesDocentic.objects.filter(cedula=cedula)
        mineducacion = DocentesMinEducacion.objects.filter(cedula=cedula)
        preinscritos = DocentesPreinscritos.objects.filter(cedula=cedula)

        redirect = '/preinscripcion/'

        if docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 1:
            redirect = '/preinscripcion/registro/'+str(cedula)

        elif docentic.count() == 0 and preinscritos.count() == 0 and mineducacion.count() == 0:
            redirect = '/preinscripcion/preregistro/'+str(cedula)

        elif docentic.count() == 1:
            if docentic[0].informatica or docentic[0].directivo:
                redirect = '/preinscripcion/diploma_reingreso/'+str(cedula)
            else:
                redirect = '/preinscripcion/diploma/'+str(cedula)

        elif preinscritos.count() == 1:
            redirect = '/encuestas/percepcionfinal/'+str(cedula)

        return HttpResponseRedirect(redirect)

class EncuestaFinalView(FormView):
    form_class = PercepcionFinalForm
    success_url = 'completo/'
    template_name = 'encuestas/percepcionfinal/nuevo.html'

    def form_valid(self, form):

        nuevo = PercepcionFinal()
        nuevo.docente_preinscrito = DocentesPreinscritos.objects.get(cedula = self.kwargs['pk'])
        nuevo.area = form.cleaned_data['area']
        nuevo.tiempo_formacion = form.cleaned_data['tiempo_formacion']
        nuevo.pregunta_1 = form.cleaned_data['pregunta_1']
        nuevo.pregunta_2 = form.cleaned_data['pregunta_2']
        nuevo.pregunta_3 = form.cleaned_data['pregunta_3']
        nuevo.pregunta_4 = form.cleaned_data['pregunta_4']
        nuevo.pregunta_5 = form.cleaned_data['pregunta_5']
        nuevo.pregunta_6 = form.cleaned_data['pregunta_6']
        nuevo.pregunta_7 = form.cleaned_data['pregunta_7']
        nuevo.pregunta_8 = form.cleaned_data['pregunta_8']
        nuevo.pregunta_9 = form.cleaned_data['pregunta_9']
        nuevo.pregunta_10 = form.cleaned_data['pregunta_10']
        nuevo.pregunta_11 = form.cleaned_data['pregunta_11']
        nuevo.pregunta_12 = form.cleaned_data['pregunta_12']
        nuevo.save()

        return HttpResponseRedirect(self.get_success_url())


class CompletoFinalView(TemplateView):
    template_name = 'encuestas/percepcionfinal/completo.html'