from django.db import models, IntegrityError
from django.utils import timezone
import random
import string
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from .signals import performance_metrics_handler
from django.contrib.auth.models import User
# Create your models here


def generate_code(city:str) -> str:
    '''
        A Method to create a unique identifier for Vendors and 
        Purchase orders. Returns code in format {3 letters}{12 digits}{3 letters}
        Process :- For vendors it takes name of the "City"
        and for purchase orders it accepts a string "ORD" and 
        then appends it with current timestamp and three random
        Uppercase English alphabets
    '''
    
    city_initials = city[:3].upper()
    english_letters = ''.join(random.choices(string.ascii_uppercase,k=3))

    timestamp = timezone.now().strftime("%d%m%y%H%M%S")
    code = city_initials + timestamp + english_letters
    return code   

class Vendor(models.Model):
    # Represents a vendor supplying goods or services.
    name = models.CharField(max_length=256, null=False, blank=False)
    contact_details = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=256, null=False, blank=False)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    vendor_code = models.CharField(max_length=18, unique=True, blank=True)

    # Overriding defualt save() method in order to generate vendor_code manually
    def save(self, *args, **kwargs):
        if not self.pk:
            self.vendor_code = generate_code(self.city)
        
        try:
            super().save(*args,**kwargs)
        except IntegrityError:
            self.save()

    def __str__(self) -> str:
        return f"{self.name} {self.city}"
    
        
        
class PurchaseOrder(models.Model):

    # Represents a purchase order for goods or services from a vendor.

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]

    po_number = models.CharField(max_length=18,unique=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(default=0)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgement_date = models.DateTimeField(null=True, blank=True)

    '''
    Using django-simple-history package to get the information about
    the previous instance which is needed for calculation of 
    performance metrics of vendors
    '''
    history = HistoricalRecords()

    # Overriding defualt save() method in order to generate po_number manually
    def save(self, *args,**kwargs):
        if not self.pk:
            self.po_number = generate_code("ORD")

        try:
            super().save(*args,**kwargs)
        except IntegrityError:
            self.save()

            
    def __str__(self) -> str:
        return self.po_number
    
class HistoricalPerformance(models.Model):

    # Represents historical performance metrics of vendors at a given time.

    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, related_name="performances")
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fullfilment_rate = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.vendor.name} performance till {str(self.date)[:10]}"
    
    '''
    Overriding the default save() method to get the snapshot of vendor performance
    metrics at current date and time (timezone.now())
    '''
    def save(self, *args, **kwargs):
        vendor = self.vendor
        self.on_time_delivery_rate = vendor.on_time_delivery_rate
        self.quality_rating_avg = vendor.quality_rating_avg
        self.average_response_time = vendor.average_response_time
        self.fullfilment_rate = vendor.fulfillment_rate

        super().save(*args, **kwargs)
    

'''
Connect post_save signal to performance_metrics_handler function for
calculation of vendor's performance metrics
'''
post_save.connect(performance_metrics_handler, sender=PurchaseOrder)

