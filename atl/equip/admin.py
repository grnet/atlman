from atl.costs.models import *
from atl.equip.models import *
from django.contrib import admin
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django import forms
from django.conf.urls.defaults import *


class ProductComponentAdmin(admin.ModelAdmin):
    list_display = ('description', 'model', 'date_of_purchase', 'qty', 'get_parent', 'get_project')
    list_filter = ('date_of_purchase', 'projectid')
    date_hierarchy = 'date_of_purchase'
    search_fields = ['description']

class ProductComponentInlineFormset(BaseInlineFormSet):
    
    def set_initial(self):

        # if post do not return initial or data are not saved
        if not self.instance._set_initial:
            return

        total = self.total_form_count()
        existing = self.queryset.count()
        self.initial = []
        for i in xrange(total):
            initial = {}
            self.initial.append(initial)
            if self.instance._populate_all and i == 0:
                initial.update({
                    'serial_number': self.instance._pending_serials[i],
                })
            if i < existing:
                continue

            initial.update({
                'description': self.instance.description,
                'price': self.instance.price,
                'totamount': self.instance.totamount,
                'vat': self.instance.vat,
                'grnet_supervisor': self.instance.children()[0].grnet_supervisor,
                'qty': self.instance.qty,
                'invoice_no': self.instance.children()[0].invoice_no,
                'assetcat': self.instance.assetcat.id
            })

            if self.instance._populate_all:
                correction = 1
            else:
                correction = 0
            if self.instance._pending_serials:
                initial.update({
                    'serial_number': self.instance._pending_serials[i - existing + correction],
                })

        
    def _construct_forms(self, *args, **kwargs):
        self.set_initial()
        return super(ProductComponentInlineFormset, self)._construct_forms(*args, **kwargs)

    def __init__(self, data=None, *args, **kwargs):
        super(ProductComponentInlineFormset, self).__init__(data, *args, **kwargs)


class ProductComponentInline(admin.StackedInline):
    model = ProductComponent
    extra = 0
    fields = ('description', 'serial_number', 'location', 'qty', 'assetcat',
    'price', 'totamount', 'vat', 'grnet_supervisor', 'notes', 'invoice_no', 'pending')
    formset = ProductComponentInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        curr_children = obj.productcomponent_set.count()
        populate_all = request.GET.get('populate_all', False)
        if populate_all == "False":
            populate_all = False
        obj._populate_all = populate_all
        obj._pending_serials = filter(bool, request.GET.get('serials','').split(","))
        self.extra = len(obj._pending_serials)
        obj._set_initial = request.method == 'GET'
        if populate_all:
            self.extra = self.extra - curr_children

        return super(ProductComponentInline, self).get_formset(request, obj, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'model', 'assetcat',
    'date_of_purchase','qty')
    list_filter = ('date_of_purchase', 'assetcat', 'model')
    search_fields = ['description']
    date_hierarchy = 'date_of_purchase'
    fields = ('description', 'companyoid','projectid','model', 'qty', 'date_of_purchase', 'invoice_no', 'assetcat', 'price', 'totamount', 'vat')
    readonly_fields=('description','companyoid','projectid','model','qty',
    'price', 'totamount', 'vat', 'assetcat', 'date_of_purchase',
    'invoice_no')
    inlines = [
        ProductComponentInline,
    ]
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DelegationAdmin(admin.ModelAdmin):
    list_display = ('description', 'product', 'delegationdate')
    list_filter = ('person', 'returndate')
    related_search_fields = {
                             'product':('description','serial_number')
                             }

class PlaceAdmin(admin.ModelAdmin):

    class Media:
        js = [
            'http://code.jquery.com/jquery-1.4.2.min.js', 
            'http://maps.google.com/maps/api/js?sensor=false', 
            settings.MEDIA_URL +'/admin/long-lat-render.js'
        ]
            
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    list_filter = ('name', 'address', )
    class Media:
        js = [
            'http://code.jquery.com/jquery-1.4.2.min.js', 
            'http://maps.google.com/maps/api/js?sensor=false', 
            settings.MEDIA_URL +'js/long-lat-render.js'
        ]

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'mobile', 'fax')
    list_filter = ('name', 'phone', 'mobile', 'fax')


class CompanyAdmin(admin.ModelAdmin):
    fields = ('company_name','description','afm','address','phone','fax','company_e_mail')

class MaintenanceForm(ModelForm):
    products=forms.ModelMultipleChoiceField(ProductComponent.objects.all(),widget=
FilteredSelectMultiple("ProductComponent",True), required=False)
    class Meta:
        model= Maintenance

class MaintenanceAdmin(admin.ModelAdmin):
    form = MaintenanceForm
    save_as = True
    
admin.site.register(Place, PlaceAdmin)
admin.site.register(Product, ProductAdmin)  
admin.site.register(ProductComponent, ProductComponentAdmin)    
#admin.site.register(ProductType)
admin.site.register(Person, PersonAdmin)
admin.site.register(Maintenance,MaintenanceAdmin)
admin.site.register(CompanyTable, CompanyAdmin)
admin.site.register(City)

admin.site.register(Delegation, DelegationAdmin)
