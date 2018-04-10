"""
WSGI config for mainblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')  
sys.path.append('/usr/local/lib64/python2.7/site-packages') 
sys.path.append('/usr/local/lib/python2.7/site-packages/frida_android_M2Crypto-0.27.0-py2.7-linux-x86_64.egg')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainblog.settings")

application = get_wsgi_application()
