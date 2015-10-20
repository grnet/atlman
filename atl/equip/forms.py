# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

from django import forms
from django.forms import ModelForm
from atl.equip.models import * 
from django.conf import settings
from django.forms.widgets import *
from django.contrib.admin import widgets
from django.contrib.auth.models import User, Group

class ProductsForm(forms.Form):
    product = forms.ModelChoiceField(queryset=ProductComponent.objects.all().order_by('description'),
            required=False,
            label=u"Προιόν",
            empty_label=u"Όλα")
    place = forms.ModelChoiceField(queryset=Place.objects.all().order_by('name'),
            required=False,
            label=u"Τοποθεσία",
            empty_label=u"Όλοι")
    prod_type = forms.ChoiceField(
        label=u"Τύπος Συσκευής",
        choices=[
            ( t['assetcat'], t['assetcat'] ) for t in
             ProductComponent.objects.values('assetcat').distinct()
        ]
    )
    coids = ProductComponent.objects.values('companyoid').distinct()
    comp_pks = [c['companyoid'] for c in coids]
    companies = Company.objects.filter(pk__in=comp_pks)
    company = forms.ChoiceField(
        label=u"Προμηθευτής",
        choices=[
            ( comp, comp) for comp in companies  
        ]
    )
    purchace_date = forms.CharField(label = "Ημερομηνία Προμήθειας grater than")
    start = forms.CharField(label = "Από")
    end = forms.CharField(label = "Έως")
    serial = forms.CharField(label = "Serial")
    return_date = forms.CharField(label = "Επιστροφη")
    
class SerialsForm(forms.Form):
    serials = forms.CharField(label='Serials', widget=forms.Textarea)
    populate_all = forms.BooleanField(label="Βάλε serial σε όλες τις εγγραφές")
