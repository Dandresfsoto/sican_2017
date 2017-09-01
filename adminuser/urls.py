from django.conf.urls import url
from adminuser.views import UserListView, UpdateUserView, NewUserView, GroupListView,NewGroupView, UpdateGrupoView,DeleteGrupoView
from adminuser.views import PermisosListView, NuevoPermisoView, EditarPermisoView, EliminarPermisoView

urlpatterns = [
    url(r'^usuarios/$', UserListView.as_view()),
    url(r'^usuarios/nuevo/$', NewUserView.as_view()),
    url(r'^usuarios/editar/(?P<pk>[0-9]+)/$', UpdateUserView.as_view()),

    url(r'^grupos/$', GroupListView.as_view()),
    url(r'^grupos/nuevo/$', NewGroupView.as_view()),
    url(r'^grupos/editar/(?P<pk>[0-9]+)/$', UpdateGrupoView.as_view()),
    url(r'^grupos/eliminar/(?P<pk>[0-9]+)/$', DeleteGrupoView.as_view()),

    url(r'^permisos/$', PermisosListView.as_view()),
    url(r'^permisos/nuevo/$', NuevoPermisoView.as_view()),
    url(r'^permisos/editar/(?P<pk>[0-9]+)/$', EditarPermisoView.as_view()),
    url(r'^permisos/eliminar/(?P<pk>[0-9]+)/$', EliminarPermisoView.as_view()),
]