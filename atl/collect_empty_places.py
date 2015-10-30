# -*- coding: utf-8 -*-
import sys, os
import settings
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place

places = Place.objects.all()
with open('deleted_unissigned_places.txt' , 'w') as f:
    for place in places:
        # if place is not assigned to any items and is not from noc api
        if place.productcomponent_set.count() == 0 and place.api_id == None:
            f.write('Deleting : {} - {}\n'.format(str(place.id), place.name.encode('utf-8')))

            # uncomment(comment) to(not) delete empty places that are not from noc api
            place.delete()
