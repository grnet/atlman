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

urlpatterns = patterns('atl.costs.views',
    # Example:
    # (r'^atl/', include('atl.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    (r'^admin/', include(admin.site.urls)),
#    (r'^$','getProjects'),
    (r'^$', 'index_page'),
    (r'^index$', 'index_page'),
    (r'^redirect_form$', 'index'),
    (r'^results$', 'results'),
    (r'^logout/$', 'logout_view'),
    (r'^costsearch/$', 'costsearch'),
    (r'^costsearch_dev/$', 'costsearch_dev'),
    (r'^tripsearch/$', 'tripsearch'),
    (r'^myprojects/$', 'myprojects'),
    url(r'^myprojectsa/$', 'myprojects', name="myprojects"),
    (r'^useraccounts/$', 'useraccounts'),
    url(r'xls/', 'to_xls', name="to_xls")    

)
urlpatterns += patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
#    (r'^getdata/$','retData'),
)
