# Django settings for atl project.
# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
import os
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
LDAP_AUTH_SETTINGS = (
    {'url': 'ldap://ds.admin.grnet.gr', 'base': 'dc=admin,dc=grnet,dc=gr'},
   # {'url': 'ldaps://ds.noc.grnet.gr',   'base': 'dc=noc,dc=grnet,dc=gr'  },
)

# If defined as a string new users will belong in this group. Group must exist
LDAP_AUTH_GROUP = None
# Whether new users will have admin access
LDAP_AUTH_IS_STAFF = False

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Athens'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'el-GR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
#USE_L10N = True
DECIMAL_SEPARATOR = ','
#THOUSAND_SEPARATOR = '.'
#USE_THOUSAND_SEPARATOR = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '//atlman.admin.grnet.gr/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'atl.djangobackends.ldapBackend.ldapBackend',
    'django.contrib.auth.backends.ModelBackend',
)


ROOT_URLCONF = 'atl.urls'

#INTERNAL_IPS = ('83.212.9.78',)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"/srv/www/atl/costs/templates/",
    #"/srv/www/atl/equip/templates/",
    "/home/tsakalos/atl/costs/templates/",
    "/home/tsakalos/atl/equip/templates/",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_extensions',
    'atl.costs',
    'atl.equip',
#    'debug_toolbar',
)

#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#)



AUTH_PROFILE_MODULE = 'costs.UserRoleProject'

LOGIN_URL='/costs/login/'
LOGIN_REDIRECT_URL = '/costs'
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25
SERVER_EMAIL = "noreply@grnet.gr"

from local_settings import *
