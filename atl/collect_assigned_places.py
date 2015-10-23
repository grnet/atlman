# -*- coding: utf-8 -*-
import sys, os
import settings
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place

places = Place.objects.all()
with open('assigned_places.txt' , 'w') as f:
    for place in places:
        if place.productcomponent_set.count() > 0:
            f.write('id: {} - name: {} with {} items\n'.format(str(place.id),\
                place.name.encode('utf-8'), str(place.productcomponent_set.count())))
