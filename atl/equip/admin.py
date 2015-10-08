from atl.costs.models import *
from atl.equip.models import *
from django.contrib import admin
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django.forms import ModelForm
from django import forms
from django.conf.urls.defaults import *

def product_component_form_factory(product):
    class RuntimeProductForm(forms.ModelForm):
        class Meta:
            model = ProductComponent
        def __init__(self, *args, **kwargs):
            kwargs['initial'] = { 'assetcat':product.assetcat}
            return super(RuntimeProductForm, self).__init__(*args, **kwargs)

    return RuntimeProductForm

class ProductComponentAdmin(admin.ModelAdmin):
    list_display = ('description', 'model', 'date_of_purchase', 'qty', 'get_parent', 'get_project')
    list_filter = ('date_of_purchase', 'projectid')
    date_hierarchy = 'date_of_purchase'
    search_fields = ['description']

class ProductComponentInline(admin.StackedInline):
    model = ProductComponent
    extra = 0
    fields = ('description', 'serial_number', 'location', 'qty', 'assetcat', 'price', 'totamount', 'vat', 'grnet_supervisor', 'notes')
    def get_formset(self, request, obj=None, **kwargs):
        if obj is not None:
            self.form = product_component_form_factory(obj)
        return super(ProductComponentInline, self).get_formset(request, obj, **kwargs)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'model', 'assetcat', 'date_of_purchase','qty')
    list_filter = ('date_of_purchase', 'assetcat', 'model')
    search_fields = ['description']
    date_hierarchy = 'date_of_purchase'
    fields = ('description', 'companyoid','projectid','model', 'qty', 'date_of_purchase', 'invoice_no', 'assetcat', 'price', 'totamount', 'vat')
    readonly_fields=('description','companyoid','projectid','model','qty', 'price', 'totamount', 'vat', 'assetcat', 'date_of_purchase', 'invoice_no')
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
