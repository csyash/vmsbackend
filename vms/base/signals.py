from django.db.models import Sum, F, ExpressionWrapper, fields
from django.utils import timezone

def performance_metrics_handler(sender, instance , created, **kwargs):
    print("inside quality rating handler")
    vendor = instance.vendor
    all_pos = vendor.orders.all()
    completed_pos = all_pos.filter(status='completed')
    previous_status = instance.history.first().status
    
    if not created:
        
        if completed_pos.count() == 0 or all_pos.count() == 0:
                print("Inside first if count=0")
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.fulfillment_rate = 0
                vendor.save()
                return
        
        #   CALCULATION OF ON TIME DELIVERY DATE
        if instance.status == 'completed' and previous_status != 'completed':
            print("Inside calc of on time delivery rate")

            pos_delivered_on_time = completed_pos.filter(delivery_date__lte=timezone.now())
            vendor.on_time_delivery_rate = pos_delivered_on_time.count() / completed_pos.count()


        #   CALCULATION OF AVERAGE QUALTITY RATING
        if instance.status == 'completed' and instance.quality_rating > 0:
            print("Inside calc of Average Quality Rating")

            pos_where_quality_was_provided = completed_pos.exclude(quality_rating=0)
            temp = pos_where_quality_was_provided.aggregate(Sum("quality_rating", default=0))
            total_sum_quality_rating = temp['quality_rating__sum']
            average_quality_rating_sum =( total_sum_quality_rating / pos_where_quality_was_provided.count())
            vendor.quality_rating_avg = average_quality_rating_sum    
                        
            
        #   CALCULATION OF AVERAGE RESPONSE TIME
        if instance.acknowledgement_date is not None:
            print("Inside calc of Average Response Time")

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
            

        #   CALCULATION OF FULLFILMENT RATE
        if instance.status is not  previous_status:
            print("Inside calc of Fullfilment Rate")

            if completed_pos.count() ==0 or all_pos.count()==0:
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.save()
                return

            vendor.fulfillment_rate = completed_pos.count() / all_pos.count()
            
            
        vendor.save()
