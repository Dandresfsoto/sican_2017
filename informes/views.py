from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from informes.models import InformesExcel


# Create your views here.
class InicioView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'informes/excel/lista.html'
    permission_required = "permisos_sican.informes.excel.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.informes.excel.crear')
        return super(InicioView, self).get_context_data(**kwargs)


class DeleteInformeView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = InformesExcel
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'formacion/cronograma/eliminar.html'
    permission_required = "permisos_sican.formacion.cronograma.eliminar"