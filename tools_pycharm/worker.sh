#!/usr/bin/env bash
source /home/sistemas/.sican/bin/activate
celery -A sican worker -l info -B