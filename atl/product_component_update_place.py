import settings
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place, ProductComponent


filename = 'correct_assignments.txt'
with open(filename, 'r') as f:
    data = f.readlines()
matches = []

for match in data:
    arr_match = match.split('->')
    curr_id = int(arr_match[0])
    api_id = int(arr_match[1])
    matches.append((curr_id, api_id))

for match in matches:
    curr = match[0]
    api_id = match[1]

    pr_components = ProductComponent.objects.filter(location=curr)
    place = Place.objects.get(api_id=api_id)
    for pr_component in pr_components:
        pr_component.location = place
        pr_component.save()
