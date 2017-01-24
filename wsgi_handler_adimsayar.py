import os, sys
import site

site.addsitedir(os.path.dirname(os.path.abspath(__file__)) + '/lib/python2.7/site-packages/')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/template/')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

project_dir_name = os.path.relpath(os.path.dirname(os.path.abspath(__file__)), '/home/ubuntu')
os.environ['PROJECT_DIR_NAME'] = project_dir_name
os.environ['DJANGO_SETTINGS_MODULE'] = project_dir_name + '.settings'
os.environ['OVERLOAD_SITE'] = 'adimsayar'
os.environ['SITE_ROOT'] = os.path.dirname(__file__)

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
