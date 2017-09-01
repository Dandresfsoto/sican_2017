#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, FormView
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from mail_templated import send_mail
from sican.settings.base import DEFAULT_FROM_EMAIL
from usuarios.models import User
import random
import string
from usuarios.tasks import send_mail_templated
from sican.forms import ConsultaBeneficiarioForm
from django.http import HttpResponseRedirect
from matrices.models import Beneficiario
from ipware.ip import get_ip
from django.utils import timezone

class Login(TemplateView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            return redirect('/proyectos/')
        else:
            if request.method == 'GET':
                context = self.get_context_data(**kwargs)
                return self.render_to_response(context)

            elif request.method == 'POST':
                context = self.get_context_data(**kwargs)
                email = request.POST['email']
                password = request.POST['password']

                user = authenticate(username=email,password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('/proyectos/')
                    else:
                        context['error'] = "Tu usuario no se encuentra activo."
                        context['email'] = email
                        return self.render_to_response(context)
                else:
                    context['error'] = "El correo electrónico y la contraseña que ingresaste no coinciden."
                    context['email'] = email
                    return self.render_to_response(context)

            else:
                return super(Login,self).dispatch(request, *args, **kwargs)

class Logout(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

class Recovery(TemplateView):
    template_name = 'recovery.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        elif request.method == 'POST':
            context = self.get_context_data(**kwargs)
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            url_base = request.META['HTTP_ORIGIN']

            if password1 != password2:
                context['email'] = email
                context['error'] = "Las contraseñas no coinciden."
                return self.render_to_response(context)
            elif password1 == "" and password2 == "":
                context['email'] = email
                context['error'] = "Ingrese una contraseña valida."
                return self.render_to_response(context)
            elif User.objects.filter(email=email).count() == 0:
                context['email'] = email
                context['error'] = "El email no esta registrado."
                return self.render_to_response(context)
            else:
                user = User.objects.get(email=email)
                user.recovery = "".join( [random.choice(string.ascii_letters) for i in xrange(15)] )
                user.new_password = password1
                user.save()
                send_mail_templated.delay('email/recovery_password.tpl', {'code':user.recovery,'url_base':url_base,'email': email,'password':password1,'fullname':user.fullname}, DEFAULT_FROM_EMAIL, [email])
                context['error'] = "Revisa tu correo electrónico y acepta el cambio de contraseña."
                return self.render_to_response(context)

        else:
            return super(Recovery,self).dispatch(request, *args, **kwargs)

class Confirmation(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        users = User.objects.filter(email=request.GET['email'])

        if users.count() == 0:
            context['error'] = "El correo electrónico no se encuentra registrado."
        else:
            user = users[0]
            if user.recovery == request.GET['code'] and user.recovery != "":
                password = user.new_password
                user.set_password(password)
                user.new_password = ""
                user.recovery = ""
                user.save()
                context['error'] = "Se realizó el cambio de contraseña de manera exitosa."

            elif user.recovery == "":
                context['error'] = "Enlace no valido, posiblemente ya cambiaste la contraseña."

        return self.render_to_response(context)

class Proyectos(LoginRequiredMixin,TemplateView):
    template_name = "proyectosmix.html"

    def get_context_data(self, **kwargs):
        kwargs['inicio'] = True
        return super(Proyectos,self).get_context_data(**kwargs)

class Diplomas(FormView):
    form_class = ConsultaBeneficiarioForm
    template_name = "diplomas/escuelatic/consulta.html"
    success_url = "/diplomas/respuesta/"

    def get_context_data(self, **kwargs):
        kwargs['inicio'] = True
        return super(Diplomas,self).get_context_data(**kwargs)

    def form_valid(self, form):
        success_url = ''
        cedula = form.cleaned_data['cedula']
        try:
            beneficiario = Beneficiario.objects.get(cedula=cedula)
        except:
            pass
        else:
            success_url = beneficiario.get_diploma_url()
            beneficiario.ip_descarga = get_ip(self.request)
            beneficiario.fecha_descarga = timezone.now()
            beneficiario.save()
        return HttpResponseRedirect(success_url)