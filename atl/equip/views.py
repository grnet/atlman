# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from atl.equip.models import *
from atl.equip.forms import SerialsForm
from datetime import *
import operator


def index(request):
    return render_to_response('equippage.html', context_instance=RequestContext(request))

def products(request):
#    assetcats = AssetCategory.objects.all().select_related()
#    assets = [asset.descr for asset in assetcats]
#    products = ProductComponent.objects.all().select_related()
#    comppks = [x.companyoid_id for x in products]
#    uniquekeys = dict(map(lambda i: (i,1),comppks)).keys()
#    companies = Company.objects.select_related().filter(pk__in=uniquekeys).order_by('company_name')
#    projpks = [x.projectid_id for x in products]
#    uniqueprojkeys = dict(map(lambda i: (i,1),projpks)).keys()
#    projects = Project.objects.filter(pk__in=uniqueprojkeys).order_by('project_name').select_related()
    #related_fields = ['companyoid', 'assetcat', 'projectid', 'assetid',
    #'parent', 'assetid__ascid']
    #related_fields = map(lambda x:x.upper(), related_fields)
    products = ProductComponent.objects.select_related('companyoid', 'assetcat', 'projectid', 'assetid',
    'parent', 'assetid__ascid')
    #products = products.filter()
    #products = products[:54] #TODO: remove this
    companies = make_unique_list(products.values_list('companyoid__company_name', flat=True))
    projs = []
    for product in products:
        if product.projectid:
            projs.append(product.projectid.project_full_name)
        else:
            projs.append(None)
    #projects = make_unique_list(products.values_list('projectid__project_name', flat=True))
    projects = make_unique_list(projs)
    assets = make_unique_list(products.values_list('assetcat__descr', flat=True))
    companies.sort()
    projects.sort()
    assets.sort()
    ret = {"products": products, "companies":companies, "projects": projects, "assetcats": assets}
    return render_to_response('products.html', ret, context_instance=RequestContext(request))


def product_details(request):
    if request.method == 'GET':
        if 'product' in request.GET:
            product_id = request.GET.get('product')
            product =  ProductComponent.objects.filter(pk=product_id).select_related()
            ret = {"product": product}
            return render_to_response('product.html', ret, context_instance=RequestContext(request))

def maintenance(request):
    maintenance = Maintenance.objects.all().select_related()
    today = datetime.today().date()
    ret = {"maintenance": maintenance, "today":today}
    return render_to_response('maintenance.html', ret, context_instance=RequestContext(request))


def delegations(request):
    delegations = Delegation.objects.all().select_related()
    ret = {"delegations": delegations}
    return render_to_response('delegations.html', ret, context_instance=RequestContext(request))

def search(request):
    products = ProductComponent.objects.all().select_related()
    ret = {"products": products}
    return render_to_response('search.html', ret, context_instance=RequestContext(request))

def make_unique_list(mylist):
    myset = set(mylist)
    return list(myset)

def serials_input(request):
    prodid = request.GET.get('prod')
    data = {'populate_all': False}
    try:
        product = Product.objects.get(id=prodid)
        if product.children().count() == 1:
            if not product.children()[0].serial_number:
                data['populate_all'] = True
    except Product.DoesNotExist:
        if not prodid:
            return redirect('/equip')
    form = SerialsForm(initial=data)
    ret = {'prodid': prodid, 'form': form}
    return render_to_response('serials.html', ret, context_instance=RequestContext(request) )

#def search_old(request):
##    if request.method == 'POST':
##        productform = ProductsForm(request.POST)
##        if productform.is_valid():
##            product = productform.cleaned_data['category']
##            cat_name = Category.objects.get(pk=category).tag
##            cidr = int(networkform.cleaned_data['cidr'])
##            allorfree = networkform.cleaned_data['allorfree']
##            showuncollapsed = networkform.cleaned_data['showuncollapsed']
##            results = {'category':  category,
##                       'catname':cat_name,
##                       'cidr': cidr,
##                       'allorfree': allorfree,
##                       'showuncollapsed': showuncollapsed
##                       }
#    prodform = ProductsForm()
#    fieldsets = (
#     ('Personal Data', {'fields':('product',), }),
#     ('Address', {'fields':('prod_type','company','purchace_date','start')}),
#    )
#    return render_to_response('search.html', {
#            'prodform': prodform, 'fieldsets' : fieldsets,         
#        },context_instance =RequestContext(request))
##    return render_to_response('search.html', context_instance=RequestContext(request))
