import sys
import os
from django.core.management import setup_environ    
import settings
setup_environ(settings)
from equip.models import *
import time


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
    print time.strftime("%d/%m/%y - %H:%M:%S") 
    if products_added > 0:
        print '{} products added'.format(str(products_added))
    else:
        print 'No products added'
    print '\n\n'

if __name__ == "__main__":
    populate()
