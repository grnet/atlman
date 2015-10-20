# -*- coding: utf-8 -*-
import sys, os
import json
import settings
import requests
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place


data_url = "https://mon.grnet.gr/api/pops/locations/"
web_data = requests.get(data_url).text
data = json.loads(web_data)
api_total = len(data)

created = 0
updated = 0
not_changed = 0
for item in data:
    
    api_id = item['id']
    name = item['name']
    address = item['address']
    
    try:
        place = Place.objects.get(api_id=api_id)
        item_updated = False
        if place.name != name:
            place.name = name
            item_updated = True
        if place.address != address:
            place.address = address
            item_updated = True
        if item_updated:
            place.save()
            updated += 1
        else:
            not_changed += 1
    except Place.DoesNotExist:
        Place.objects.create(api_id=api_id, 
                             name=name,
                             address=address)
        created += 1

print "Api total places: {}".format(str(api_total))
print "Places created: {}".format(str(created))
print "Places updated: {}".format(str(updated))
print "Places not_changed: {}".format(str(not_changed))
