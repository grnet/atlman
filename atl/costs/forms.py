# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

from django import forms
from django.forms import ModelForm
from atl.costs.models import * 
from django.conf import settings
from django.forms.widgets import *
from django.contrib.admin import widgets
from django.contrib.auth.models import User, Group

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class myCalendarWidget(forms.TextInput):
    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.4/jquery-ui.js')

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        
class AccountsForm(forms.Form):
    def __init__(self, username, *args, **kwargs):
        super(AccountsForm, self).__init__(*args, **kwargs)
        user = User.objects.get(username=username)
        code_tags = [x.pk for x in user.get_profile().project.all()]
        if user.get_profile().role.role == 'Administrator':
            returned_objects = Customerjob.objects.all()
        else:
            returned_objects = Customerjob.objects.filter(pk__in=code_tags)
        customerjobs=returned_objects.order_by('code')
        
        allcustjobs = [(customerjob.pk, "%s - %s" % (customerjob.code, customerjob.descr)) for customerjob in customerjobs]
        allcustjobs.insert(0,('all','Όλα'))
        self.fields['selcustjob'] = forms.ChoiceField(
                                label = "Έργο",
                                choices = allcustjobs,
                                required=False)
        self.fields['resultstype'] = forms.ChoiceField(
                                    choices=[['showcosts','Δαπανών'],['showpayments','Πληρωμών']], 
                                    label = "Προβολή",
                                    )
        self.fields['start'] = forms.CharField(label = "Από")
        self.fields['end'] = forms.CharField(label = "Έως")

        
class TripsForm(forms.Form):
    def __init__(self, username, *args, **kwargs):
        super(TripsForm, self).__init__(*args, **kwargs)
        user = User.objects.get(username=username)
        code_tags = [x.pk for x in user.get_profile().project.all()]
        if (user.get_profile().role.role == 'Administrator'):
            returned_objects = Customerjob.objects.all()
        else:
            returned_objects = Customerjob.objects.filter(pk__in=code_tags)
        customerjobs=returned_objects.order_by('code')
        
        allcustjobs = [(customerjob.pk, "%s - %s" % (customerjob.code, customerjob.descr)) for customerjob in customerjobs]
        allcustjobs.insert(0,('all','Όλα'))
        self.fields['selcustjob'] = forms.ChoiceField(
                                label = "Έργο",
                                choices = allcustjobs,
                                required=False)
        self.fields['resultstype'] = forms.ChoiceField(
                                    choices=[['showcosts','Δαπανών'],['showpayments','Πληρωμών']], 
                                    label = "Προβολή",
                                    )
        self.fields['start'] = forms.CharField(label = "Από")
        self.fields['end'] = forms.CharField(label = "Έως")
        
class UserAccountForm(ModelForm):
    class Meta:
        model = UserProjectDetails
        exclude = ('user','project')

        
