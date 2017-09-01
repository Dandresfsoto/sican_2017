#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sican.celery import app
from time import sleep
from celery import task, current_task

@app.task
def add():
    for value in range(10000):
        sleep(0.1)
        current_task.update_state(state="PROGRESS",meta={'current': value})

