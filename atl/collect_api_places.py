# -*- coding: utf-8 -*-
#! /usr/bin/env python

import sys, os
import settings
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place

places = Place.objects.all()
with open('api_places.txt' , 'w') as f:
    for place in places:
        if place.api_id != None:
            f.write('id: {} - api_id: {} - name: {}\n'.format(str(place.id),
                str(place.api_id), place.name.encode('utf-8')))
