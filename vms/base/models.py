from django.db import models
from django.utils import timezone
import random
import string
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models import Sum, F, ExpressionWrapper, fields
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
    name = models.CharField(max_length=256, null=False, blank=False)
    contact_details = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=256)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    vendor_code = models.CharField(max_length=7, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.vendor_code = generate_code(self.city)
        
        super().save(*args,**kwargs)

    def __str__(self) -> str:
        return f"{self.name} {self.city}"
    
        
        
class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]

    po_number = models.CharField(max_length=256,unique=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(default=0)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgement_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args,**kwargs):
        if not self.pk:
            self.po_number = generate_code("ORD")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.po_number
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, related_name="performances")
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fullfilment_rate = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.vendor.name} performance till {str(self.date)[:10]}"
    

previous = {}

@receiver(pre_save, sender=PurchaseOrder)
def handler(sender, instance, *args, **kwargs):
    if instance.pk:
        previous_instance = PurchaseOrder.objects.get(pk=instance.pk)
        previous[instance.pk] = previous_instance.status
        return


@receiver(post_save, sender=PurchaseOrder)
def quality_rating_handler(sender, instance : PurchaseOrder, created, **kwargs):
    vendor:Vendor = instance.vendor
    all_pos = vendor.orders.all()
    completed_pos = all_pos.filter(status='completed')
    previous_status = previous[instance.pk]
    previous.clear()

    if not created:

        #   CALCULATION OF AVERAGE QUALTITY RATING
        if instance.status == 'completed' and instance.quality_rating != 0:
            
            if completed_pos.count() == 0:
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.average_response_time = 0
                vendor.fulfillment_rate = 0
                vendor.save()
                return
            
            pos_where_quality_was_provided = completed_pos.exclude(quality_rating=0)
            temp = pos_where_quality_was_provided.aggregate(Sum("quality_rating", default=0))
            total_sum_quality_rating = temp['quality_rating__sum']
            average_quality_rating_sum =( total_sum_quality_rating / pos_where_quality_was_provided.count())

            vendor.quality_rating_avg = average_quality_rating_sum                
            
        #   CALCULATION OF AVERAGE RESPONSE TIME
        if instance.acknowledgement_date is not None:

            if all_pos.count() == 0:
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.average_response_time = 0
                vendor.fulfillment_rate = 0
                vendor.save()
                return
            
            total_response_time = all_pos.aggregate(total_response_time=Sum(ExpressionWrapper(F('acknowledgement_date') - F('issue_date'), output_field=fields.DurationField())))['total_response_time']
            if total_response_time is not None:
                average_response_time = total_response_time.total_seconds()/all_pos.count()
                vendor.average_response_time = average_response_time
            else:
                vendor.average_response_time = 0
            

        #   CALCULATION OF ON TIME DELIVERY DATE
        if instance.status == 'completed' and previous_status != 'completed':
            pos_delivered_on_time = completed_pos.filter(delivery_date__lte=timezone.now())

            if completed_pos.count() ==0:
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.save()
                return

            vendor.on_time_delivery_rate = pos_delivered_on_time.count() / completed_pos.count()

        #   CALCULATION OF FULLFILMENT RATE
        if instance.status != previous_status:

            if completed_pos.count() ==0 or all_pos.count()==0:
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.save()
                return

            vendor.fulfillment_rate = completed_pos.count() / all_pos.count()
            
            
        vendor.save()
        return








