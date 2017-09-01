#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from celery import shared_task
from mail_templated import send_mail


@shared_task
def send_mail_templated(template,dictionary,from_email,list_to_email):
    send_mail(template, dictionary, from_email, list_to_email)
    return 'Email send'

@shared_task
def add(x, y):
    return x + y