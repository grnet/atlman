from atl.costs.models import *
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django import forms
    
#admin.site.register(Company)
#admin.site.register(Project)
#admin.site.register(Customerjob)



#admin.site.register(ProductType)
#admin.site.register(UserRole)

class UserRoleForm(ModelForm):
    project=forms.ModelMultipleChoiceField(Customerjob.objects.all(),widget=
            FilteredSelectMultiple("Customerjob",True), required=False)
    class Meta:
        model= UserRoleProject

class UserRoleProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'role',)
    form = UserRoleForm



class UserProjectDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'project',)


#class ProductAdmin(admin.ModelAdmin):
#    list_display = ('description', 'model', 'product_type', 'date_of_purchase')
#    list_filter = ('date_of_purchase', 'product_type', 'model', 'guarantee')
#    search_fields = ['description']
#
#admin.site.register(Product, ProductAdmin)

#class DelegationAdmin(admin.ModelAdmin):
#    list_display = ('description', 'product', 'supervisor', 'delegationdate')
#    list_filter = ('person', 'supervisor', 'project', 'returndate')
#    
#admin.site.register(Delegation, DelegationAdmin)

#class PlaceAdmin(admin.ModelAdmin):
#    list_display = ('name', 'address')
#    list_filter = ('name', 'address', )
#admin.site.register(Place, PlaceAdmin)

#class PersonAdmin(admin.ModelAdmin):
#    list_display = ('name', 'phone', 'mobile', 'fax')
#    list_filter = ('name', 'phone', 'mobile', 'fax')

#class desiredAccountsAdmin(admin.ModelAdmin):
#    list_display = ('descr','get_accounts')

#
#admin.site.register(Person, PersonAdmin)
#admin.site.register(Account)
#admin.site.register(desiredAccounts, desiredAccountsAdmin)
# admin.site.register(UserProjectDetails, UserProjectDetailsAdmin)

admin.site.register(UserRoleProject, UserRoleProjectAdmin)
#admin.site.register(UserRoleProjectAccount, UserRoleProjectAccountAdmin)
