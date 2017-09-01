from django.conf.urls import url
from contratos import views

urlpatterns = [
    #-----------------------------------------------LEGALIZACION--------------------------------------------------------
    url(r'^legalizacion/$', views.LegalizacionContratosView.as_view()),
    #----------------------------------------------ADMINISTRATIVOS------------------------------------------------------
    url(r'^legalizacion/administrativos/$', views.LegalizacionContratosAdministrativosView.as_view()),
    #-------------------------------------------------FORMADORES--------------------------------------------------------
    url(r'^legalizacion/formadores/$', views.LegalizacionContratosFormadoresView.as_view()),
    url(r'^legalizacion/formadores/contrato/(?P<id_contrato>[0-9]+)/$', views.LegalizacionContratoFormadorView.as_view()),
    #---------------------------------------------------LIDERES---------------------------------------------------------
    url(r'^legalizacion/lideres/$', views.LegalizacionContratosLideresView.as_view()),
    url(r'^legalizacion/lideres/contrato/(?P<id_contrato>[0-9]+)/$', views.LegalizacionContratoLiderView.as_view()),
    #-------------------------------------------------NEGOCIADORES------------------------------------------------------
    url(r'^legalizacion/negociadores/$', views.LegalizacionContratosNegociadoresView.as_view()),
    url(r'^legalizacion/negociadores/contrato/(?P<id_contrato>[0-9]+)/$', views.LegalizacionContratoNegociadorView.as_view()),
    #-------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------SEGURIDAD SOCIAL---------------------------------------------------
    url(r'^seguridadsocial/$', views.SeguridadSocialView.as_view()),
    #----------------------------------------------ADMINISTRATIVOS------------------------------------------------------
    url(r'^seguridadsocial/administrativos/$', views.SeguridadSocialAdministrativosView.as_view()),
    #-------------------------------------------------FORMADORES--------------------------------------------------------
    url(r'^seguridadsocial/formadores/$', views.SeguridadSocialFormadoresView.as_view()),
    url(r'^seguridadsocial/formadores/contrato/(?P<id_contrato>[0-9]+)/$', views.SeguridadSocialFormadorView.as_view()),
    #-------------------------------------------------------------------------------------------------------------------
]