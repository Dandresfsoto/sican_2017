"""sican URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sican.views import Login, Logout, Recovery, Confirmation, Proyectos, Diplomas
from sican.settings import base as settings
from sican.settings import dev as develop_settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^adminuser-sican/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', Login.as_view(),name='login'),
    url(r'^logout/', Logout.as_view()),
    url(r'^recovery/$', Recovery.as_view()),
    url(r'^recovery/confirmation/$', Confirmation.as_view()),
    url(r'^proyectos/', Proyectos.as_view()),
    url(r'^usuario/', include('usuarios.urls', namespace='usuarios')),
    #url(r'^realtime/', include('inbox.urls', namespace='inbox')),
    url(r'^rest/', include('rest.urls', namespace='rest')),
    url(r'^rh/', include('rh.urls', namespace='rh')),
    url(r'^adminuser/', include('adminuser.urls', namespace='adminuser')),
    url(r'^bases/', include('bases.urls', namespace='bases')),
    url(r'^preinscripcion/', include('preinscripcion.urls', namespace='preinscripcion')),
    url(r'^formadores/', include('formadores.urls', namespace='formadores')),
    url(r'^financiera/', include('financiera.urls', namespace='financiera')),
    url(r'^informes/', include('informes.urls', namespace='informes')),
    url(r'^formacion/', include('formacion.urls', namespace='formacion')),
    url(r'^encuestas/', include('encuestas.urls', namespace='encuestas')),
    url(r'^messenger/', include('messenger.urls', namespace='messenger')),
    url(r'^lideres/', include('lideres.urls', namespace='lideres')),
    url(r'^estrategia/', include('productos.urls', namespace='productos')),
    url(r'^acceso/', include('acceso.urls', namespace='acceso')),
    url(r'^matrices/', include('matrices.urls', namespace='matrices')),
    url(r'^evidencias/', include('evidencias.urls', namespace='evidencias')),
    url(r'^requerimientos/', include('requerimientos.urls', namespace='requerimientos')),
    url(r'^diplomas/', Diplomas.as_view()),
    url(r'^negociadores/', include('negociadores.urls', namespace='negociadores')),
    url(r'^contratos/', include('contratos.urls', namespace='contratos')),
    #url(r'^sicantelegram/', include('telegrambot.urls', namespace="telegrambot")),
    url(r'^processing/', include('permabots.urls_processing', namespace="permabots")),
    url(r'^api/v1/', include('permabots.urls_api', namespace="api")),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^beneficiarios/', include('beneficiarios.urls', namespace='beneficiarios')),
    url(r'^vigencia2017/', include('vigencia2017.urls', namespace='vigencia2017')),
]

if settings.DEBUG:
    urlpatterns += static(develop_settings.MEDIA_URL, document_root=develop_settings.MEDIA_ROOT)