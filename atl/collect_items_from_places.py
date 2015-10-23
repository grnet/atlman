# -*- coding: utf-8 -*-
import sys, os
import settings
from django.core.management import setup_environ
setup_environ(settings)
from equip.models import Place

place_names = ["«Άγιος Γρηγόριος ο Παλαμάς»", "Αποθήκη ΕΔΕΤ",
               "Δημ.Παν.Θράκης–Πολ/κή Σχολή Αλεξανδρούπολης", "Δημοκρίτειο Πανεπιστήμιο Θράκης",
               "Δημοκρίτειο Πανεπιστήμιο Θράκης – Κομοτηνή", "Δήμος Αντιγονιδών",
               "ΕΜΠ (Κτίριο Ηλ. Υπολογιστή, Γραφείο 111)", "ΕΜΠ (Νέο κτήριο Ηλεκτρολόγων, Γραφείο Β.3.20)", 
               "Ερευν. Παν. Ινστ. Επιτ. Συσ. & Εφαρμ. (ΙΕΣΕ)", "Τέστ",
               "Τηλεπικοινωνιακό κέντρο ΟΤΕ - Πρέβεζα", "Φορέας-8: Εθνικό Μετσόβιο Πολυτεχνείο"]

with open("place_to_items.txt", "w") as f:
    for name in place_names:
        place = Place.objects.get(name=name)
        f.write("Place id: {} - name: {}\n".format(str(place.id), place.name.encode('utf-8')))
        f.write("    items number: {}\n".format(str(place.productcomponent_set.count())))
        f.write("    Items:\n")
        for item in place.productcomponent_set.all():
            f.write("       id: {} - Description: {} - Model: {}\n".format(str(item.id),
                                                                           item.description.encode('utf-8'),
                                                                           item.model.encode('utf-8')))
            f.write("\n")

        f.write("\n\n")
