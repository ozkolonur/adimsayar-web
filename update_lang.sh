#!/bin/sh

django-admin.py makemessages -l tr
django-admin.py makemessages -l en
django-admin.py compilemessages
cd userprofile
django-admin.py compilemessages
cd ..

