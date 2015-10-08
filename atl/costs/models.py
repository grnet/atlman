# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

    
class Customerjob(models.Model):
    id = models.IntegerField(db_column='id',primary_key=True)
    code = models.CharField(db_column='code',max_length=25)
    descr = models.CharField(db_column='descr',max_length=200)
    
    def getScwebAccounts(self):
        return Scwebkartela.objects.filter(cjoid=self).distinct('acccode').order_by('acccode').values('acccode')
    
    class Meta:
        db_table = u'CUSTOMERJOB'
        verbose_name = u'Έργο'        
        verbose_name_plural = u'Έργα'
        ordering = ['code']
    def __unicode__(self):
        return "%s %s" %(self.code,self.descr)
    
class AssetCategory(models.Model):
    id = models.IntegerField(db_column='codeid',primary_key=True)
    descr = models.CharField(db_column='descr',max_length=200)

    class Meta:
        db_table = u'ASSETCATEGORY'
        verbose_name = u'Κατηγορία Παγίου'
        verbose_name_plural = u'Κατηγορίες Παγίων'
        ordering = ['descr']
    def __unicode__(self):
        return "%s" %(self.descr)

class Asset(models.Model):
    id = models.IntegerField(db_column='id',primary_key=True)
    code = models.CharField(db_column='code',max_length=25)
    descr = models.CharField(db_column='descr',max_length=200)
    ascid = models.ForeignKey(AssetCategory, db_column='ascid',max_length=200)

    class Meta:
        db_table = u'ASSET'
        verbose_name = u'Πάγιο'
        verbose_name_plural = u'Πάγια'
        ordering = ['code']
    def __unicode__(self):
        return "%s %s" %(self.code,self.descr)

class Account(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    code = models.CharField(db_column='code',max_length=25)
    descr = models.CharField(db_column='descr',max_length=200)
    
    def getScwebCjs(self):
        return Scwebkartela.objects.filter(accid=self).distinct('code').order_by('code').values('code')
    
    class Meta:
        db_table = u'ACCOUNT'
        verbose_name = u'Λογαριασμός'        
        verbose_name_plural = u'Λογαριασμοί'
        ordering = ['code']
    def __unicode__(self):
        return "%s - %s" %(self.code, self.descr)

class desiredAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    descr = models.CharField(max_length=100)
    account = models.ManyToManyField(Account)

    class Meta:
        db_table = u'desaccounts'
        verbose_name = u'Επιθυμητος Λογαριασμός'        
        verbose_name_plural = u'Επιθυμητοί Λογαριασμοί'
    
    def get_accounts(self):
        tags = ", ".join([a.__str__() for a in self.account.all()])
        return tags
    

    def __unicode__(self):
        return self.descr

class Scwebkartela(models.Model):
    flg = models.CharField(db_column='flg', max_length=2)
    accid = models.ForeignKey(Account, db_column='accid') # Field name made lowercase.
    acccode = models.CharField(Account, db_column='acccode', max_length=25) # Field name made lowercase.
    code = models.CharField(db_column='code', max_length=25) # Field name made lowercase.
    cjoid = models.ForeignKey(Customerjob, db_column='cjoid') # Field name made lowercase.
    descr = models.CharField(max_length=200, null=True, db_column='descr', blank=True) # Field name made lowercase.
    ftrid = models.IntegerField(db_column='FTRID', primary_key=True) # Field name made lowercase.
    tradecode = models.CharField(max_length= 30, null=True, db_column='tradecode', blank=True) # Field name made lowercase.
    ftrdate = models.DateTimeField(null=True, db_column='ftrdate', blank=True) # Field name made lowercase.
    cover = models.DecimalField(null=True, db_column='cover', blank=True, decimal_places=2, max_digits=200) # Field name made lowercase.
    cover_fx = models.FloatField(null=True, db_column='cover_fx', blank=True) # Field name made lowercase.
    dapani = models.DecimalField(null=True, db_column='dapani', blank=True, decimal_places=2, max_digits=200) # Field name made lowercase.
    dsrid = models.IntegerField(db_column='dsrid') # Field name made lowercase.
    supname = models.CharField(null=True, db_column='supname', blank=True, max_length=50) # Field name made lowercase.
    afm = models.CharField(null=True, db_column='afm', blank=True, max_length=50) # Field name made lowercase.
    sc_rel_ftr = models.IntegerField(db_column='sc_rel_ftr') # Field name made lowercase.
    comid = models.IntegerField(db_column='comid') # Field name made lowercase.
    foreigndescr = models.CharField(null=True, db_column='foreigndescr', blank=True, max_length=255) # Field name made lowercase.
    trip_code = models.CharField(null=True, db_column='trip_code', blank=True, max_length=15) # Field name made lowercase.
    trip_description = models.CharField(null=True, db_column='trip_description', blank=True, max_length=60) # Field name made lowercase.
    datestart = models.DateTimeField(null=True, db_column='datestart', blank=True) # Field name made lowercase.
    datestop = models.DateTimeField(null=True, db_column='datestop', blank=True) # Field name made lowercase.
    sortdescr = models.CharField(null=True, db_column='sortdescr', blank=True, max_length=50) # Field name made lowercase.
    trip_remarks = models.CharField(null=True, db_column='trip_remarks', blank=True, max_length=50) # Field name made lowercase.
    sc_travelexpenses = models.IntegerField(db_column='sc_travelexpenses') # Field name made lowercase.
    expdescr = models.CharField(null=True, db_column='expdescr', blank=True, max_length=1000) # Field name made lowercase.
    sc_puserid = models.IntegerField(db_column='sc_puserid') # Field name made lowercase.
    sftrdate = models.CharField(null=True, db_column='sftrdate', blank=True, max_length=20) # Field name made lowercase.

    class Meta:
        db_table = u'SC_WEB_KARTELA_4'
        unique_together = ('ftrid', 'acccode')
    
    def __unicode__(self):
        return self.descr

class Company(models.Model):
    id = models.IntegerField(primary_key=True, db_column='oid_2') # Field name made lowercase.
    company_name = models.TextField(db_column='company_name', blank=True, max_length=200) # Field name made lowercase.
    description = models.TextField(db_column='description', blank=True, max_length=200) # Field name made lowercase. This field type is a guess.
    afm = models.TextField(db_column='afm', blank=True, max_length=200) # Field name made lowercase.
    address = models.TextField(db_column='address', blank=True, max_length=200) # Field name made lowercase.
    phone = models.TextField(db_column='phone', blank=True, max_length=200) # Field name made lowercase.
    fax = models.TextField(db_column='fax', blank=True, max_length=200) # Field name made lowercase.
    company_e_mail = models.TextField(db_column='company_e_mail', blank=True, max_length=200) # Field name made lowercase.
    class Meta:
        db_table = u'companytable_37'
        verbose_name = u'Εταιρία'   
        verbose_name_plural = u'Εταιρίες'
    def __unicode__(self):
        return self.company_name


class Project(models.Model):
    id = models.IntegerField(primary_key=True, db_column='oid_2') # Field name made lowercase.
    project_name = models.TextField(null=True,db_column='project_name', blank=True, max_length=200) # Field name made lowercase.
    description = models.TextField(null=True,db_column='description', blank=True, max_length=200) # Field name made lowercase. This field type is a guess.
    termination = models.DateTimeField(null=True,db_column='termination', blank=True, max_length=200) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'projecttable_37'
        ordering = ['project_name']
    def __unicode__(self):
        return "%s:%s" %(self.get_code(), self.project_name)
    
    def get_code(self):
        try:
            cj = Customerjob.objects.get(descr = self.project_name)
            code = cj.code
        except:
            code= "---"
        return code

    def _get_full_project_name(self):
        return "%s:%s" %(self.get_code(), self.project_name) 
    project_full_name = property(_get_full_project_name)

    

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(max_length=15, blank=True, null=True)
    mobile = models.IntegerField(max_length=15, blank=True, null=True)
    fax = models.IntegerField(max_length=15, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = u'persontable'
        verbose_name = u'Υπεύθυνος'   
        verbose_name_plural = u'Υπεύθυνοι'
    def __unicode__(self):
        return self.name

class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(db_column='role',max_length=25)
    class Meta:
        db_table = u'userrole'
        verbose_name = u'Ρόλος Χρήστη'        
        verbose_name_plural = u'Ρόλοι Χρηστών'
    def __unicode__(self):
        return self.role

class Customerjob_hack(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    code = models.CharField(db_column='code',max_length=25)
    descr = models.CharField(db_column='descr',max_length=200)
    
    class Meta:
        db_table = u'CUSTOMERJOB'
        verbose_name = u'Έργο'        
        verbose_name_plural = u'Έργα'
        ordering = ['code']

    def __unicode__(self):
        return "%s %s" %(self.code,self.descr)

class UserRoleProject(models.Model):
    user = models.ForeignKey(User, primary_key=True, db_column='userid')
    role =  models.ForeignKey(UserRole, blank=True, null=True)
    project = models.ManyToManyField(Customerjob, blank=True, null=True)
    class Meta:
        db_table = u'userroleproject'
        verbose_name = u'Ρόλος Χρήστη σε Έργο'        
        verbose_name_plural = u'Ρόλοι Χρηστών σε Έργα'
        
    def count_projects(self):
        if self.role == 'Administrator':
            projects = [x for x in Customerjob.objects.all()]
        else:
            projects = [x for x in self.project.all()]
        return len(projects)

class UserRoleProjectAccount(models.Model):
    user = models.ForeignKey(User, primary_key=True, db_column='userid')
    role =  models.ForeignKey(UserRole, blank=True, null=True)
    project = models.ManyToManyField(Customerjob, blank=True, null=True)
    account = models.ManyToManyField(Account, blank=True, null=True)
    class Meta:
        db_table = u'userroleprojectaccount'
        verbose_name = u'Ρόλος Χρήστη σε Έργο - Λογαριασμοί'        
        verbose_name_plural = u'Ρόλοι Χρηστών σε Έργα - Λογαριασμοί'
        
    def count_projects(self):
        if self.role == 'Administrator':
            projects = [x for x in Customerjob.objects.all()]
        else:
            projects = [x for x in self.project.all()]
        return len(projects)
    
    def count_accounts(self):
        if self.role == 'Administrator':
            accounts = [x for x in Account.objects.all()]
        else:
            accounts = [x for x in self.account.all()]
        return len(accounts)

class UserProjectDetails(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, db_column='userid')
    project = models.ForeignKey(Customerjob, db_column='project')
    account = models.ManyToManyField(Account, db_column='account')
    class Meta:
        db_table = u'userprojectdetails'
        verbose_name = u'Λογαριασμοί Χρήστη σε Έργο'        
        verbose_name_plural = u'Λογαριασμοί Χρηστών σε Έργα'

#class UserRoleProjectNew(User):
#    role =  models.ForeignKey(UserRole, blank=True, null=True)
#    project = models.ManyToManyField(Customerjob_hack, blank=True, null=True)
#    class Meta:
#        db_table = u'userroleprojectnew'
#        verbose_name = u'Ρόλος Χρήστη σε Έργο'        
#        verbose_name_plural = u'Ρόλοι Χρηστών σε Έργα'
