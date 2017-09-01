from django.conf.urls import url
from requerimientos.views import RequerimientosListView, NuevoRequerimientoView, UpdateRequerimientoView, DeleteRequerimientoView

urlpatterns = [
    url(r'^delegacion/$', RequerimientosListView.as_view()),
    url(r'^delegacion/nuevo/$', NuevoRequerimientoView.as_view()),
    url(r'^delegacion/editar/(?P<pk>[0-9]+)/$', UpdateRequerimientoView.as_view()),
    url(r'^delegacion/eliminar/(?P<pk>[0-9]+)/$', DeleteRequerimientoView.as_view()),
]