# -*- coding: utf-8 -*-
import sys, os
import settings
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place

places = Place.objects.all()
with open('unissigned_places_with_noc.txt' , 'w') as f:
    for place in places:
        #if place.productcomponent_set.count() == 0:
        if place.productcomponent_set.count() == 0 and place.api_id == None:
            f.write('{} - {}\n'.format(str(place.id), place.name.encode('utf-8')))
