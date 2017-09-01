#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from acceso.models import Retoma
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML

class RetomaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RetomaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Radicado',
                    Div(
                        Div('radicado',css_class='col-sm-6'),
                        css_class='row'
                    ),
                    Div(
                        Div(
                            HTML(
                                """
                                <p>Radicado:<p/>
                                <p>Municipio:<p/>
                                <p>Dane:<p/>
                                <p>Ubicación:<p/>
                                <p>Institución:<p/>
                                <p>Sede:<p/>
                                """
                            ),
                            css_class='col-sm-12'
                        ),
                        css_class='row'
                    ),

                ),
                css_class = 'row'
            )
        )

    class Meta:
        model = Retoma
        fields = '__all__'