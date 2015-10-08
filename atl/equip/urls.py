# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('atl.equip.views',
    # Example:
    # (r'^atl/', include('atl.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    (r'^admin/', include(admin.site.urls)),
#    (r'^$','getProjects'),
    (r'^$', 'index'),
    (r'^products/$', 'products'),
    (r'^maintenance/$', 'maintenance'),
    (r'^delegations/$', 'delegations'),
    (r'^search/$', 'search'),
    (r'^product/$', 'product_details'),
   

)
