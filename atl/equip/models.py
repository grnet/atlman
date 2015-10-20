# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
from django.db import models
from django.contrib.auth.models import User, Group
from atl.costs.models import *
import django.dispatch
from datetime import *

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,blank=True, null=True, verbose_name="Ονομασία")
    country = models.CharField(max_length=255,blank=True, null=True, default="Ελλάδα")
    class Meta:
        db_table = u'equip_city'
        verbose_name = u'Πόλη'        
        verbose_name_plural = u'Πόλεις'
        ordering = ['name']
    def __unicode__(self):
        return self.name
   
# Create your models here.
class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Ονομασία")
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name="Διεύθυνση")
    city = models.ForeignKey(City, blank=True, null=True, db_column='city', verbose_name="Πόλη")
    phone = models.IntegerField(max_length=15, blank=True, null=True, verbose_name="Τηλέφωνο")
    fax = models.IntegerField(max_length=15, blank=True, null=True, verbose_name="Fax")
    mail = models.CharField(max_length=50, blank=True, null=True, verbose_name="E-mail")
    
    class Meta:
        db_table = u'placetable'
        verbose_name = u'Τοποθεσία'        
        verbose_name_plural = u'Τοποθεσίες'
        ordering = ['name']
    def __unicode__(self):
        return self.name

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Ονομαteπώνυμο")
    phone = models.IntegerField(max_length=15, blank=True, null=True, verbose_name="Τηλέφωνο")
    mobile = models.IntegerField(max_length=15, blank=True, null=True, verbose_name="Κινητό")
    fax = models.IntegerField(max_length=15, blank=True, null=True, verbose_name="Fax")
    mail = models.CharField(max_length=50, blank=True, null=True, verbose_name="E-mail")
    company = models.CharField(max_length=50, blank=True, null=True, verbose_name="Εταιρία")
    
    class Meta:
        db_table = u'persontable'
        verbose_name = u'Ανθρώπινο Δυναμικό'   
        verbose_name_plural = u'Ανθρώπινο Δυναμικό'
        ordering = ['name']
    def __unicode__(self):
        return self.name
 
class Company(models.Model):
    id = models.IntegerField(primary_key=True, db_column='OID_2') # Field name made lowercase.
    company_name = models.TextField(db_column='COMPANY_NAME', blank=True, max_length=200, verbose_name="Ονομασία") # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True, max_length=200, verbose_name="Περιγραφή") # Field name made lowercase. This field type is a guess.
    afm = models.TextField(db_column='AFM', blank=True, max_length=200, verbose_name="ΑΦΜ") # Field name made lowercase.
    address = models.TextField(db_column='ADDRESS', blank=True, max_length=200, verbose_name="Διεύθυνση") # Field name made lowercase.
    phone = models.TextField(db_column='PHONE', blank=True, max_length=200, verbose_name="Τηλέφωνο") # Field name made lowercase.
    fax = models.TextField(db_column='FAX', blank=True, max_length=200, verbose_name="Fax") # Field name made lowercase.
    company_e_mail = models.TextField(db_column='COMPANY_E_MAIL', blank=True, max_length=200, verbose_name="Email Εταιρίας") # Field name made lowercase.
    class Meta:
        db_table = u'companytable_37'
        verbose_name = u'Εταιρία Προμήθειας'   
        verbose_name_plural = u'Εταιρίες Προμήθειας'
        ordering = ['company_name']
    def __unicode__(self):
        return self.company_name
    def populate_companies(self):
        try:
            isindb = CompanyTable.objects.get(company_name = self.company_name)
        except:
            newcompany = CompanyTable(
                                related_company = self.id,
                                company_name = self.company_name,
                                description = self.description,
                                afm = self.afm,
                                address = self.address,
                                phone = self.phone,
                                fax = self.fax,
                                company_e_mail = self.company_e_mail,
                            )
            newcompany.save()

class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    
    class Meta:
        db_table = u'producttypetable'
        verbose_name = u'Είδος Προϊόντος'
        verbose_name_plural = u'Είδη Προϊόντων'
        ordering = ['type']
    def __unicode__(self):
        return self.type

product_component_imported = django.dispatch.Signal(providing_args=["model"])
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True, db_column='Id') # Field name made lowercase.
    oid = models.IntegerField(db_column='OID_2') # Field name made lowercase.
    model = models.CharField(null=True,db_column='MODEL', blank=True, max_length=200, verbose_name="Μοντέλο") # Field name made lowercase.
    #guarantee = models.DateTimeField(null=True, db_column='GUARANTEE', blank=True, verbose_name="the related poll") # Field name made lowercase. This field type is a guess.
    price = models.FloatField(null=True, db_column='PRICE', blank=True, max_length=200, verbose_name="Τιμή μονάδας (χωρίς ΦΠΑ)") # Field name made lowercase.
    qty = models.FloatField(null=True, db_column='QTY', blank=True, max_length=200, verbose_name="Ποσότητα") # Field name made lowercase.
    date_of_purchase = models.DateTimeField(null=True,db_column='DATE_OF_PURCHASE', blank=True, verbose_name="Ημ/νία Προμήθειας") # Field name made lowercase. This field type is a guess.
    #serial_number = models.CharField(null=True,db_column='SERIAL_NUMBER', blank=True, max_length=200, verbose_name="Σειριακός Αριθμός") # Field name made lowercase.
    description = models.CharField(null=True,db_column='DESCRIPTION', blank=True, max_length=200, verbose_name="Περιγραφή") # Field name made lowercase.
    companyoid = models.ForeignKey(Company, db_column='COMPANYOID', blank=True , null=True, verbose_name="Εταιρία") # Field name made lowercase.
    #product_type = models.ForeignKey(ProductType, null=True, db_column='PRODUCT_TYPEOID', blank=True, max_length=200, verbose_name="Κατηγορία Παγίου") # Field name made lowercase.
#    preservation = models.DateTimeField(null=True,db_column='PRESERVATION', blank=True) # Field name made lowercase. This field type is a guess.
#    status = models.CharField(null=True,db_column='STATUS', blank=True, max_length=200) # Field name made lowercase.
    invoice_no = models.TextField(null=True,db_column='INVOICE_NO', blank=True, max_length=200) # Field name made lowercase.
    assetid = models.ForeignKey(Asset, null=True, db_column='ASSETID', blank=True ) # Field name made lowercase.
    assetcat = models.ForeignKey(AssetCategory, null=True, db_column='ASSETCAT', blank=True ) # Field name made lowercase.
    projectid = models.ForeignKey(Project, db_column='PROJECTID', blank=True, null=True, verbose_name="Έργο") # Field name made lowercase.
    vat = models.FloatField(db_column='VAT', blank=True, max_length=200, verbose_name="ΦΠΑ") # Field name made lowercase.
    totamount = models.FloatField(null=True, db_column='TOTAMOUNT', blank=True, max_length=200, verbose_name="Σύνολο") # Field name made lowercase.
    class Meta:
        db_table = u'producttable_37'
        verbose_name = u'Πάγιο Δεξαμενής'
        verbose_name_plural = u'Δεξαμενή Παγίων (Προσθήκη Components)'
        ordering = ['description']
        
    def __unicode__(self):
        return u"%s" %self.description
    
    def children(self):
        return ProductComponent.objects.filter(parent=self)

    def populate_components(self):
        if self.children().count() == 0:
            newcomponent = ProductComponent(
                                            parent = self,
                                            model = self.model,
                                            #guarantee = self.guarantee,
                                            price = self.price,
                                            qty = self.qty,
                                            date_of_purchase = self.date_of_purchase,
                                            #serial_number = self.serial_number,
                                            description = self.description,
                                            companyoid = self.companyoid,
                                            #product_type = self.product_type,
                                            location = None,
                                            grnet_supervisor = None,
                                            #preservation = self.preservation,
                                            #status = self.status,
                                            invoice_no = self.invoice_no,
                                            assetid = self.assetid,
                                            assetcat = self.assetcat,
                                            projectid = self.projectid,
                                            vat = self.vat,
                                            totamount = self.totamount
                                        )
            newcomponent.save()
            product_component_imported.send(sender=self, model=self.description)
        else:
            pass
    

class ProductComponent(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Product)
    model = models.CharField(null=True,db_column='MODEL', blank=True, max_length=200, verbose_name="Μοντέλο") # Field name made lowercase.
    #guarantee = models.DateTimeField(null=True, db_column='GUARANTEE', blank=True) # Field name made lowercase. This field type is a guess.
    price = models.FloatField(null=True, db_column='PRICE', blank=True, max_length=200, verbose_name="Τιμή μονάδας (χωρίς ΦΠΑ)") # Field name made lowercase.
    qty = models.FloatField(null=True, db_column='QTY', blank=True, max_length=200, verbose_name="Ποσότητα") # Field name made lowercase.
    date_of_purchase = models.DateTimeField(null=True,db_column='DATE_OF_PURCHASE', blank=True, verbose_name="Ημ/νία Προμήθειας") # Field name made lowercase. This field type is a guess.
    serial_number = models.CharField(null=True,db_column='SERIAL_NUMBER', blank=True, max_length=200, verbose_name="Σειριακός Αριθμός") # Field name made lowercase.
    description = models.CharField(null=True,db_column='DESCRIPTION', max_length=200, verbose_name="Περιγραφή") # Field name made lowercase.
    companyoid = models.ForeignKey(Company, db_column='COMPANYOID', blank=True , null=True, verbose_name="Εταιρία") # Field name made lowercase.
    #product_type = models.ForeignKey(ProductType, null=True, db_column='PRODUCT_TYPEOID', blank=True, max_length=200, verbose_name="Κατηγορία Παγίου") # Field name made lowercase.
    location = models.ForeignKey(Place, null=True, db_column='LOCATION', blank=True, verbose_name="Τοποθεσία") # Field name made lowercase.
    grnet_supervisor = models.ForeignKey(Person, null=True, db_column='GRNET_SUPERVISOR', verbose_name="Υπεύθυνος ΕΔΕΤ", blank=True)
#    preservation = models.DateTimeField(null=True,db_column='PRESERVATION', blank=True) # Field name made lowercase. This field type is a guess.
#    status = models.CharField(null=True,db_column='STATUS', blank=True, max_length=200) # Field name made lowercase.
    invoice_no = models.TextField(null=True,db_column='INVOICE_NO', blank=True, max_length=200) # Field name made lowercase.
    assetid = models.ForeignKey(Asset, null=True, db_column='ASSETID', blank=True ) # Field name made lowercase.
    assetcat = models.ForeignKey(AssetCategory, null=True, db_column='ASSETCAT', blank=True ) # Field name made lowercase.
    projectid = models.ForeignKey(Project, db_column='PROJECTID', blank=True , null=True, verbose_name="Έργο") # Field name made lowercase.
    vat = models.FloatField(db_column='VAT', blank=True, max_length=200, verbose_name="ΦΠΑ") # Field name made lowercase.
    totamount = models.FloatField(null=True, db_column='TOTAMOUNT', blank=True, max_length=200, verbose_name="Σύνολο") # Field name made lowercase.
    notes = models.TextField(null=True, db_column='NOTES', blank=True, verbose_name="Σημειώσεις") # Field name made lowercase.

    class Meta:
        db_table = u'productcomponenttable_37'
        verbose_name = u'Πάγιο'
        verbose_name_plural = u'Πάγια (Components)'
        ordering = ['description']

#    def get_type(self):
#        return self.product_type.type

    def get_parent(self):
        return self.parent.description

    get_parent.short_description = 'Parent Product'
    get_parent.admin_order_field = 'parent__description'

    def get_project(self):
        return self.projectid.project_name

    get_project.short_description = 'Project'
    get_project.admin_order_field = 'projectid__project_name'
    
    def _get_full_project_name(self):
        if self.projectid:
            return "%s:%s" %(self.projectid.get_code(), self.projectid.project_name)
        else:
            return None
    project_full_name = property(_get_full_project_name)

    @property
    def amount_no_vat(self):
        return self.totamount - self.vat

    def __unicode__(self):
        return u"%s" %self.description

    @property
    def is_in_maintenance(self):
        maintenances = self.maintenance_set.all()
        ret = False
        if len(maintenances) > 0:
            for maintenance in maintenances:
                if maintenance.enddate > datetime.today().date():
                    ret = True
                else:
                    continue
        return ret

    def save(self, *args, **kwargs):
        self.model = self.parent.model
        self.assetid = self.parent.assetid
        self.companyoid = self.parent.companyoid
        self.projectid = self.parent.projectid
        self.date_of_purchase = self.parent.date_of_purchase
        super(ProductComponent, self).save(*args,**kwargs)

class Delegation(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    product = models.ForeignKey(ProductComponent, blank=True, null=True, verbose_name="Πάγιο")
    person = models.ForeignKey(Person, blank=True, null=True, verbose_name="Ανατέθηκε στον/στην")
    deltio_apostolis = models.CharField(max_length=255, blank=True, null=True, verbose_name="Δελτίο Αποστολής")
    location = models.ForeignKey(Place, null=True, blank=True, db_column='location', verbose_name="Τοποθεσία")
    delegationdate = models.DateField(blank=True, null=True, verbose_name="Ημερομηνία Ανάθεσης")
    returndate = models.DateField(blank=True, null=True, verbose_name="Ημερομηνία Επιστροφής")
    handed_by = models.ForeignKey(Person, blank=True, null=True, related_name="handed_by", db_column='handed_by', verbose_name="Παραδόθηκε από")
    returnconfirmation = models.BooleanField(default=False, verbose_name="Έχει επιστραφεί")
    
    
    class Meta:
        db_table = u'delegationtable'
        verbose_name = u'Ανάθεση'        
        verbose_name_plural = u'Αναθέσεις'
    def __unicode__(self):
        return self.description
    
class CompanyTable(models.Model):
    id = models.AutoField(primary_key=True, db_column='OID_2') # Field name made lowercase.
    related_company =  models.IntegerField(db_column='RELATED_COMPANY_OID_2', null=True, blank=True) # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME',null=True, blank=True, max_length=200) # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION',null=True, blank=True, max_length=200) # Field name made lowercase. This field type is a guess.
    afm = models.CharField(db_column='AFM', null=True, blank=True, max_length=200) # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS',null=True, blank=True, max_length=200) # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', null=True, blank=True, max_length=200) # Field name made lowercase.
    fax = models.CharField(db_column='FAX', null=True, blank=True, max_length=200) # Field name made lowercase.
    company_e_mail = models.CharField(db_column='COMPANY_E_MAIL', null=True, blank=True, max_length=200) # Field name made lowercase.
    class Meta:
        db_table = u'companytable'
        ordering = ['company_name']
        verbose_name = u'Εταιρία'   
        verbose_name_plural = u'Εταιρίες'
    def __unicode__(self):
        return self.company_name

class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, verbose_name="Περιγραφή")
    companyoid = models.ForeignKey(CompanyTable, db_column='COMPANYOID', blank=True , null=True, verbose_name="Εταιρία") # Field name made lowercase.
    protocol_num = models.CharField(max_length=255, blank=True, null=True, verbose_name="Αριθμός Πρωτοκόλλου")
    startdate = models.DateField(blank=True, null=True, verbose_name="Ημερομηνία Έναρξης")
    enddate = models.DateField(blank=True, null=True, verbose_name="Ημερομηνία Λήξης")
    totamount = models.FloatField(null=True, db_column='TOTAMOUNT', blank=True, verbose_name="Σύνολο") # Field name made lowercase.
    products = models.ManyToManyField(ProductComponent, blank=True, null=True, verbose_name="Προϊόντα")
    
    
    class Meta:
        db_table = u'maintenance_table'
        verbose_name = u'Συντήρηση'        
        verbose_name_plural = u'Συντηρήσεις'
    def __unicode__(self):
        return self.description
