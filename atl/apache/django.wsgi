# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

import os, sys
sys.path.append('/srv/www/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'atl.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
