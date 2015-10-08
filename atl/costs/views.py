# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
# Create your views here.
from atl.costs.models import *
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from atl.costs.forms import *
from django.template import RequestContext
from django.core.context_processors import request
from django.db.models import Avg, Max, Min, Count, Sum
from datetime import datetime, date, time
from django.contrib.auth import logout
import pprint
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from decimal import *
import xlwt
from xlwt import *

@login_required
def index(request):
    return render_to_response('page.html', context_instance=RequestContext(request))

@login_required
def index_page(request):
    return render_to_response('page.html', context_instance=RequestContext(request))

@login_required
def myprojects(request):
    if request.user.is_authenticated():
        user = request.user
        username = user.username
        try:
            userrole = UserRoleProject.objects.filter(user__username=username).get()
        except:
            logout(request)
            next_page = reverse(index)
            return HttpResponseRedirect(next_page)
        user_role = userrole.role.role
        if user_role == 'Administrator':
            projects = [x for x in Customerjob.objects.all()]
            projmsg = True
        else:
            try:
                projects = [x for x in UserRoleProject.objects.filter(user__username=username).get().project.select_related(depth=6)]
                if len(projects) == 0:
                    projmsg = False
                else:
                    projmsg = True
            except:
                projects = None
                projmsg = False
        ret = {'userprojects': projects, 'projmsg': projmsg}
        return render_to_response('welcome.html', ret, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    if request.method == 'GET':
        if 'next' in request.GET:
            next_page = request.GET.get('next')
    else:
        next_page = reverse(index)
    return HttpResponseRedirect(next_page)

@login_required
def costsearch(request):
    if request.user.is_authenticated():
        username = request.user.username 
        costsform = AccountsForm(username)
        ret = { 'costsform': costsform  }
        return render_to_response('costs.html', ret, context_instance=RequestContext(request))

@login_required
def costsearch_dev(request):
    if request.method == 'GET':
        username = request.user.username 
        costsform = AccountsForm(username)
        ret = { 'costsform': costsform  }
        return render_to_response('costs_dev.html', ret, context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
            xls_requested = False
            try:
                res_query_dict = request.session.get('toxls')
            except:
                res_query_dict = None
            if request.method == 'POST':
                if 'get_xls' in request.POST:
                    xls_requested = True
                    request.POST = res_query_dict
                reqdets ={}
                if request.user.is_authenticated():
                    user = request.user
                    username = user.username
                if request.POST.__contains__('trips'):
                    accountform = TripsForm(username, request.POST)
                if request.POST.__contains__('costs'):
                    accountform = AccountsForm(username, request.POST)
                if accountform.is_valid():
                    resultstype = accountform.cleaned_data['resultstype']
                    if request.POST.__contains__('trips'):
                        trips = True
                        accountid = 'all'
                        if (resultstype == 'showcosts'):
                            reqdets['type'] = u"Ταξίδια/Δαπάνες"
                        if (resultstype == 'showpayments'):
                            reqdets['type'] = u"Ταξίδια/Πληρωμές"
                    else:
                        trips = False
                        if (resultstype == 'showcosts'):
                            reqdets['type'] = u"Έργα/Δαπάνες"
                        if (resultstype == 'showpayments'):
                            reqdets['type'] = u"Έργα/Πληρωμές"
        #                accountid = accountform.cleaned_data['selacc']
                    projlist = []
                    filter_project_list =[]
                    filter_account_list =[]
                    projectid = accountform.cleaned_data['selcustjob']
                    startdate = accountform.cleaned_data['start']
                    enddate = accountform.cleaned_data['end']
                    reqdets['start'] = startdate
                    reqdets['end'] = enddate
                    
                    if (startdate):
                        startdate = datetime.strptime("%s 00:00"%(startdate), "%d/%m/%Y %H:%M")
                    if (enddate):
                        enddate = datetime.strptime("%s 23:59"%(enddate), "%d/%m/%Y %H:%M")
                    if request.user.is_authenticated():
                        username = request.user.username
                    if (projectid=='all'):
                        reqdets['project'] = u'Ολα τα έργα'
                    else: 
                        reqdets['project'] = u'%s' % Customerjob.objects.select_related(depth=6).get(pk=projectid)
                    if (trips):
        #                we get all trip accounts
                        filter_account_list = user_trips_accounts(username)
                        if (projectid=='all'):
                            filter_project_list = desired_user_trip_projects(username)
                        else:
                            filter_project_list.append(projectid)
                    else:
        ##                Not valid anymore, as user selects specific accounts per projects
        #                filter_account_list = [int(x) for x in accountid]
                        if (projectid=='all'):
                            filter_project_list = user_projects(username)
                        else:
                            filter_project_list.append(projectid)
                    projects = Customerjob.objects.filter(pk__in=filter_project_list).select_related()
                    projaccountsmaster = Scwebkartela.objects.select_related().filter(cjoid__in=filter_project_list).filter(ftrdate__gte=startdate).filter(ftrdate__lte=enddate).order_by('ftrdate')
                    if (trips):
                        projaccountsmaster = projaccountsmaster.filter(accid__in=filter_account_list)
                    if len(projaccountsmaster) == 0:
                        return render_to_response('results.html', context_instance=RequestContext(request))
                    upd = UserProjectDetails.objects.filter(user=user).select_related('project','account','user')
                    for b in upd:
                        b.user = user
                    accounts_all = Account.objects.all().select_related(depth=10)
                    for project in projects:                
                        if (trips):
                            projaccounts = projaccountsmaster.filter(cjoid=project.pk).distinct('trip_code').order_by('trip_code').values_list('trip_code', 'trip_description')
                        else:
                            try:
                                userprojectaccounts = upd.get(user=user, project=project).account.all()
                                if len(userprojectaccounts) == 0:
                                    continue
                            except:
                                continue
                            useraccountlist = [x.pk for x in userprojectaccounts]
                            projaccounts = projaccountsmaster.filter(cjoid=project.pk).filter(accid__in=useraccountlist).distinct('accid').order_by('accid').values_list('accid')
                        if (len(projaccounts)==0):
                            continue
                        projcost = 0
                        projdict={}
                        acclist=[]
                        projdict['project_code']=project.code
                        projdict['project_descr']=project.descr
                        for projaccount in projaccounts:
                            accdict ={}
        #                    In case of trips accounts stands for trip code whereas account_descr stands for trip description
                           
                            if (trips):
                                accdict['account'] = projaccount[0]
                                if not accdict['account']:
                                    continue
                                accdict['account_descr'] = projaccount[1]
                                if not accdict['account_descr']:
                                    continue
                            else:
                                acc_item = accounts_all.get(pk=projaccount[0])
                                accdict['account'] = acc_item.code
                                accdict['account_descr'] = acc_item.descr
                            if (trips):
                                projaccountdets = projaccountsmaster.filter(cjoid=project.pk).filter(trip_code=projaccount[0]).exclude(trip_code=None).select_related(depth=6)
                            else:
                                projaccountdets = projaccountsmaster.filter(cjoid=project.pk).filter(accid=projaccount[0]).select_related(depth=6)
                            projacclist = []
                            cost = 0;
                            if len(projaccountdets) == 0:
                                continue
                            for projaccountdet in projaccountdets:
        #                        Select whether to show dapanes or plirwmes
                                if (resultstype == 'showcosts'):
                                    showcosttype = projaccountdet.dapani
                                if (resultstype == 'showpayments'):
                                    showcosttype = projaccountdet.cover
                                details = {'ftrdate':projaccountdet.ftrdate.strftime("%d/%m/%Y"),
                                           'tradecode':projaccountdet.tradecode,
                                           'supname':projaccountdet.supname,
                                           'afm':projaccountdet.afm,
                                           'cost': showcosttype
        
                                           }
        #                        FIXME: Have to find out why this is here
                                if (projaccountdet.dapani == 0) and (projaccountdet.cover == 0):
                                    continue
                                if (trips):
                                    details['trip'] = projaccountdet.trip_description
                                    details['trip_code'] = projaccountdet.trip_code
                                cost = cost + showcosttype
        
                                if cost == 0 and (projaccountdet.dapani == 0) and (projaccountdet.cover == 0):
                                    continue
                                projacclist.append(details)
                                accdict['details'] = projacclist
        
                            if cost == 0 and (projaccountdet.dapani == 0) and (projaccountdet.cover == 0):
                                continue
                            accdict['acctotal'] = cost
                            projcost = projcost+cost
                            acclist.append(accdict)
                        if (projcost == 0):
                            continue
                        projdict['accounts'] = acclist
                        projdict['projtotal'] = projcost
                        projlist.append(projdict)
                else:
                    print accountform.errors
                    
                ret = { 'projlist':projlist, 'reqdets':reqdets}
                if xls_requested:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=results.xls'
                    # XLS generator function is called here with project as argument
                    wb = to_xls(projlist, reqdets)
                    wb.save(response)
                    return response
                request.session['toxls'] = request.POST.copy()
                return render_to_response('results_dev.html', ret, context_instance=RequestContext(request))

@login_required
def tripsearch(request):
    if request.user.is_authenticated():
        username = request.user.username 
        tripsform = TripsForm(username)
        ret = { 'tripsform': tripsform }
        return render_to_response('trips.html', ret, context_instance=RequestContext(request))

@login_required
def useraccounts(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            user=request.user
            useraccountform = UserAccountForm(request.POST)
            project=Customerjob.objects.get(pk=request.POST.get('project'))
            if useraccountform.is_valid():
                accounts = useraccountform.cleaned_data['account']
                try:
                    useraccountsall = UserProjectDetails.objects.get(user=user, project=project)
                    userform = UserAccountForm(request.POST, instance = useraccountsall)
                    userform.save()
    #                Ok, user has already a record....
                except:
                    userform = UserAccountForm(request.POST)
                    useraccountsall = userform.save(commit=False)
                    useraccountsall.user=user
                    useraccountsall.project=project
                    useraccountsall.save()
                    userform.save_m2m()
                
                userform.save()
            else:
                print accountform.errors
            return render_to_response('useraccounts.html', context_instance=RequestContext(request))
        if request.method == 'GET':
            project=Customerjob.objects.get(pk=request.GET.get('project'))
#        try to fetch existing associations
            try:
                user=request.user
                useraccountsall = UserProjectDetails.objects.get(user=user, project=project)
    #            Load existing
                costsform = UserAccountForm(instance=useraccountsall)
            except:
    #            Create New
                costsform = UserAccountForm()
            ret = { 'accountform': costsform,  'project':project}
            return render_to_response('useraccounts.html', ret, context_instance=RequestContext(request))

@login_required
def useraccounts_old(request):
    if request.user.is_authenticated():
        username = request.user.username
        if request.method == 'POST':
            costsform = UserAccountForm(username, request.POST)
            if costsform.is_valid():
                user = User.objects.filter(username=username)
                user_definition = costsform.save(commit=False)
                user_definition.user = User.objects.get(username=username)
                user_definition.save()
                costsform.save_m2m()
                return render_to_response('useraccounts.html', context_instance=RequestContext(request))
        else:
            costsform = UserAccountForm(username)
            ret = { 'accountform': costsform  }
        return render_to_response('useraccounts.html', ret, context_instance=RequestContext(request))

@login_required
def results(request):
    xls_requested = False
    try:
        res_query_dict = request.session.get('toxls')
    except:
        res_query_dict = None
    if request.method == 'POST':
        if 'get_xls' in request.POST:
            xls_requested = True
            request.POST = res_query_dict
        reqdets ={}
        if request.user.is_authenticated():
            user = request.user
            username = user.username
        if request.POST.__contains__('trips'):
            accountform = TripsForm(username, request.POST)
        if request.POST.__contains__('costs'):
            accountform = AccountsForm(username, request.POST)
        if accountform.is_valid():
            resultstype = accountform.cleaned_data['resultstype']
            if request.POST.__contains__('trips'):
                trips = True
                accountid = 'all'
                if (resultstype == 'showcosts'):
                    reqdets['type'] = u"Ταξίδια/Δαπάνες"
                if (resultstype == 'showpayments'):
                    reqdets['type'] = u"Ταξίδια/Πληρωμές"
            else:
                trips = False
                if (resultstype == 'showcosts'):
                    reqdets['type'] = u"Έργα/Δαπάνες"
                if (resultstype == 'showpayments'):
                    reqdets['type'] = u"Έργα/Πληρωμές"
#                accountid = accountform.cleaned_data['selacc']
            projlist = []
            filter_project_list =[]
            filter_account_list =[]
            projectid = accountform.cleaned_data['selcustjob']
            startdate = accountform.cleaned_data['start']
            enddate = accountform.cleaned_data['end']
            reqdets['start'] = startdate
            reqdets['end'] = enddate
            
            if (startdate):
                startdate = datetime.strptime("%s 00:00"%(startdate), "%d/%m/%Y %H:%M")
            if (enddate):
                enddate = datetime.strptime("%s 23:59"%(enddate), "%d/%m/%Y %H:%M")
            if request.user.is_authenticated():
                username = request.user.username
            if (projectid=='all'):
                reqdets['project'] = u'Ολα τα έργα'
            else: 
                reqdets['project'] = u'%s' % Customerjob.objects.get(pk=projectid)
            if (trips):
#                we get all trip accounts
                filter_account_list = user_trips_accounts(username)
                if (projectid=='all'):
                    filter_project_list = desired_user_trip_projects(username)
                else:
                    filter_project_list.append(projectid)
            else:
##                Not valid anymore, as user selects specific accounts per projects
#                filter_account_list = [int(x) for x in accountid]
                if (projectid=='all'):
                    filter_project_list = user_projects(username)
                else:
                    filter_project_list.append(projectid)
            projects = Customerjob.objects.filter(pk__in=filter_project_list)
            if (trips):
                projaccountsmaster = Scwebkartela.objects.filter(accid__in=filter_account_list).filter(cjoid__in=filter_project_list).filter(ftrdate__gte=startdate).filter(ftrdate__lte=enddate).order_by('ftrdate').select_related('accid', 'cjoid')
            else:
                projaccountsmaster = Scwebkartela.objects.filter(cjoid__in=filter_project_list).filter(ftrdate__gte=startdate).filter(ftrdate__lte=enddate).order_by('ftrdate').select_related('accid', 'cjoid')
            if len(projaccountsmaster) == 0:
                return render_to_response('results.html', context_instance=RequestContext(request))
            for project in projects:                
                if (trips):
                    projaccounts = projaccountsmaster.filter(cjoid=project.pk).distinct('trip_code').order_by('trip_code').values_list('trip_code', 'trip_description')
                else:
                    try:
                        userprojectaccounts = UserProjectDetails.objects.get(user=user, project=project).account.all()
                        if len(userprojectaccounts) == 0:
                            continue
                    except:
                        continue
                    useraccountlist = [x.pk for x in userprojectaccounts]
                    projaccounts = projaccountsmaster.filter(cjoid=project.pk).filter(accid__in=useraccountlist).distinct('accid').order_by('accid').values_list('accid')
                if (len(projaccounts)==0):
                    continue
                projcost = 0
                projdict={}
                acclist=[]
                projdict['project_code']=project.code
                projdict['project_descr']=project.descr
                for projaccount in projaccounts:
                    accdict ={}
#                    In case of trips accounts stands for trip code whereas account_descr stands for trip description
                   
                    if (trips):
                        accdict['account'] = projaccount[0]
                        if not accdict['account']:
                            continue
                        accdict['account_descr'] = projaccount[1]
                        if not accdict['account_descr']:
                            continue
                    else:
                        accdict['account'] = Account.objects.get(pk=projaccount[0]).code
                        accdict['account_descr'] = Account.objects.get(pk=projaccount[0]).descr
                    if (trips):
                        projaccountdets = projaccountsmaster.filter(cjoid=project.pk).filter(trip_code=projaccount[0]).exclude(trip_code=None)
                    else:
                        projaccountdets = projaccountsmaster.filter(cjoid=project.pk).filter(accid=projaccount[0])
                    projacclist = []
                    cost = 0;
                    if len(projaccountdets) == 0:
                        continue
                    for projaccountdet in projaccountdets:
#                        Select whether to show dapanes or plirwmes
                        if (resultstype == 'showcosts'):
                            showcosttype = projaccountdet.dapani
                        if (resultstype == 'showpayments'):
                            showcosttype = projaccountdet.cover
                        details = {'ftrdate':projaccountdet.ftrdate.strftime("%d/%m/%Y"),
                                   'tradecode':projaccountdet.tradecode,
                                   'supname':projaccountdet.supname,
                                   'afm':projaccountdet.afm,
                                   'cost': showcosttype

                                   }
#                        FIXME: Have to find out why this is here
                        if (projaccountdet.dapani == 0) and (projaccountdet.cover == 0):
                            continue
                        if (trips):
                            details['trip'] = projaccountdet.trip_description
                            details['trip_code'] = projaccountdet.trip_code
                        cost = cost + showcosttype

                        if cost == 0 and (projaccountdet.dapani == 0) and (projaccountdet.cover == 0):
                            continue
                        projacclist.append(details)
                        accdict['details'] = projacclist

                    if cost == 0 and (projaccountdet.dapani == 0) and (projaccountdet.cover == 0):
                        continue
                    accdict['acctotal'] = cost
                    projcost = projcost+cost
                    acclist.append(accdict)
                if (projcost == 0):
                    continue
                projdict['accounts'] = acclist
                projdict['projtotal'] = projcost
                projlist.append(projdict)
        else:
            print accountform.errors
            
        ret = { 'projlist':projlist, 'reqdets':reqdets}
        if xls_requested:
            response = HttpResponse(mimetype="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=results.xls'
            # XLS generator function is called here with project as argument
            wb = to_xls(projlist, reqdets)
            wb.save(response)
            return response
        request.session['toxls'] = request.POST.copy()
        return render_to_response('results.html', ret, context_instance=RequestContext(request))

def to_xls(projlist, reqdets):
    style0 = xlwt.easyxf('font: color-index red, bold on', num_format_str='###0,00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    styleColumnHeadings = easyxf('font: color-index black, bold on,italic off,height 200;''alignment: wrap True,vertical top;')
    styleHeader = easyxf('font: color-index black, bold on,height 150;''pattern: pattern solid, fore-colour grey25;''alignment: horizontal center;')
    styleSubHeader = easyxf('font: color-index black, bold on,height 150;''pattern: pattern solid, fore-colour grey25;''alignment: horizontal center;')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Projects')
    i = 0
    ws.write(i,0,u'Αποτελέσματα', styleSubHeader)
    ws.write(i,1,u'Έργο', styleSubHeader)
    ws.write(i,2,u'Από', styleSubHeader)
    ws.write(i,3,u'Έως', styleSubHeader)
    i = 1
    ws.write(i,0,reqdets['type'])
    ws.write(i,1,reqdets['project'])
    ws.write(i,2,reqdets['start'])
    ws.write(i,3,reqdets['end'])
    i = 2
    ws.write(i,0,u'Ημερομηνία', styleSubHeader)
    ws.write(i,1,u'Κωδικός/ΑΠΥ', styleSubHeader)
    ws.write(i,2,u'Ονοματεπώνυμο', styleSubHeader)
    ws.write(i,3,u'ΑΦΜ', styleSubHeader)
    ws.write(i,4,u'Ποσό', styleSubHeader)
    ws.write(i,5,u'Έργο', styleSubHeader)
    ws.write(i,6,u'Κωδικός Έργου', styleSubHeader)
    ws.write(i,7,u'Είδος Δαπάνης/Κατηγορία', styleSubHeader)
    ws.write(i,8,u'Κωδικός Δαπάνης', styleSubHeader)
    i=i+1
    for project in projlist:
#        i = 1
#        ws = wb.add_sheet(project['project_descr'])
#        
#        ws.write(i,0,u"Κωδικός Έργου",styleHeader)
#        ws.write_merge(i,i,1,2,u"Περιγραφή Έργου",styleHeader)                
#        ws.write(i,3,u"Σύνολο",styleHeader)
#        i=i+1
#        ws.write(i,0,project['project_code'])
#        ws.write_merge(i,i,1,2,project['project_descr'])                
#        ws.write(i,3,project['projtotal'],style0)
#        i = i+1
        for account in project['accounts']:
#            ws.write(i,0,u"Κωδικός Δαπάνης", styleSubHeader)
#            ws.write_merge(i,i,1,2,u"Περιγραφή Δαπάνης", styleSubHeader)   
#            ws.write(i,3,u"Υποσύνολο κατηγορίας", styleSubHeader)
#            i = i + 1
#            ws.write(i,0,account['account'], styleSubHeader)
#            ws.write_merge(i,i,1,2,account['account_descr'], styleSubHeader)   
#            ws.write(i,3,account['acctotal'], styleSubHeader)
#            i = i+1
            for detail in account['details']:
                ws.write(i,0,detail['ftrdate'])
                ws.write(i,1,detail['tradecode'])
                ws.write(i,2,detail['supname'])
                ws.write(i,3,detail['afm'])
                ws.write(i,4,detail['cost'])
                ws.write(i,5,project['project_descr'])
                ws.write(i,6,project['project_code'])
                ws.write(i,7, account['account_descr'])
                ws.write(i,8, account['account'])
                i = i+1
    return wb

def trip_accounts():
    tripaccounts = [x[0] for x in Scwebkartela.objects.exclude(trip_code=None).distinct('accid').order_by('accid').values_list('accid')]
    return tripaccounts

def user_trips_accounts(username):
    project_list = desired_user_trip_projects(username)
    usertripaccounts = [x[0] for x in Scwebkartela.objects.exclude(trip_code=None).filter(cjoid__in=project_list).distinct('accid').order_by('accid').values_list('accid')]
    return usertripaccounts

def trip_projects():
    tripcodes = [x[0] for x in Scwebkartela.objects.exclude(trip_code=None).distinct('cjoid').order_by('cjoid').values_list('cjoid')]
    return tripcodes

def desired_pagia_accounts():
    desired_accounts = desiredAccounts.objects.filter(descr='pagia')
    for des_account in desired_accounts:
        des_acc_list = des_account.account.all()
    des_acc_codelist = [x.pk for x in des_acc_list]
    return des_acc_codelist

def desired_pagia_projects():
    pagia_accounts = desired_pagia_accounts()
    desired_projects = [x[0] for x in Scwebkartela.objects.filter(accid__in=pagia_accounts).distinct('cjoid').order_by('cjoid').values_list('cjoid')]
    return desired_projects

def desired_user_pagia_projects(username):
    user_projects_list = user_projects(username)
    desired_pagia_projects_list = desired_pagia_projects()
    desired_user_pagia_projects_list = filter(lambda x:x in user_projects_list,desired_pagia_projects_list)
    return desired_user_pagia_projects_list

def desired_user_trip_projects(username):
    user_projects_list = user_projects(username)
    trip_projects_list = trip_projects()
    desired_user_trip_projects_list = filter(lambda x:x in user_projects_list,trip_projects_list)
    return desired_user_trip_projects_list

def desired_user_pagia_accounts(username):
    project_list = desired_user_pagia_projects(username)
    userpagiaaccounts = [x[0] for x in Scwebkartela.objects.filter(code__in=project_list).distinct('accid').order_by('accid').values_list('accid')]
    return userpagiaaccounts

def user_projects(username):
    user = User.objects.get(username=username)
    if (user.get_profile().role.role == 'Administrator'):
       returned_objects = Customerjob.objects.all().select_related(depth=10)
       code_tags = [x.pk for x in returned_objects]
    else:
       code_tags = [x.pk for x in user.get_profile().project.all()]
    return code_tags

def project_accounts(project_code):
    project_accounts = [x[0] for x in Scwebkartela.objects.filter(code=project_code).distinct('accid').order_by('accid').values_list('accid')]
    return project_accounts
