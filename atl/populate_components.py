import sys
import os
from django.core.management import setup_environ    
import settings
setup_environ(settings)
from django.core.mail import send_mail
from equip.models import *


products_added = 0

def my_handler(sender, **kwargs):
    global products_added
    descr = kwargs['model']
    products_added = products_added + 1

def populate():
    global products_added
    product_component_imported.connect(my_handler, dispatch_uid="mysavefunc")
    a = Product.objects.all()
    for b in a:
        b.populate_components()
    if products_added > 0:
        send_mail('%s Products Added'% products_added, '%s new products were added. Please check http://atlman.admin.grnet.gr/equip'% products_added , 'noreply@grnet.gr', ['leopoul@noc.grnet.gr'])


if __name__ == "__main__":
    populate()
