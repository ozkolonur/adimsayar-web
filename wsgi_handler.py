import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/template/')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


os.environ['DJANGO_SETTINGS_MODULE'] = 'adimsayar_org.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()