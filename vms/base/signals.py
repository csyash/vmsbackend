from django.db.models import Sum, F, ExpressionWrapper, fields
from django.utils import timezone

def performance_metrics_handler(sender, instance, created, **kwargs):
    """
    Calculates and updates performance metrics of a vendor based on changes to purchase orders.

    Args:
        sender: The model class sending the signal.
        instance: The instance of the model class that triggered the signal.
        created (bool): Indicates whether a new instance was created.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    Process:
        - Calculates and updates the on-time delivery rate.
        - Calculates and updates the average quality rating.
        - Calculates and updates the average response time.
        - Calculates and updates the fulfillment rate.
    """
    
    
    # Retrieve the vendor associated with the purchase order
    vendor = instance.vendor
    
    # Retrieve all purchase orders for the vendor
    all_pos = vendor.orders.all()
    
    # Retrieve completed purchase orders for the vendor
    completed_pos = all_pos.filter(status='completed')
    
    # Retrieve the previous status of the purchase order
    previous_status = instance.history.first().status if not created else None
    
    if not created:

          # Calculate and update average response time
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
                average_response_time = total_response_time.total_seconds() / all_pos.count()
                vendor.average_response_time = average_response_time
            else:
                vendor.average_response_time = 0


        if completed_pos.count() == 0 or all_pos.count() == 0:
            print("Inside first if count=0")
            vendor.on_time_delivery_rate = 0
            vendor.quality_rating_avg = 0
            vendor.fulfillment_rate = 0
            vendor.save()
            return
        
        # Calculate and update on-time delivery rate
        if instance.status == 'completed' and previous_status != 'completed':
            print("Inside calc of on time delivery rate")
            pos_delivered_on_time = completed_pos.filter(delivery_date__lte=timezone.now())
            vendor.on_time_delivery_rate = pos_delivered_on_time.count() / completed_pos.count()

        # Calculate and update average quality rating
        if instance.status == 'completed' and instance.quality_rating > 0:
            print("Inside calc of Average Quality Rating")
            pos_where_quality_was_provided = completed_pos.exclude(quality_rating=0)
            temp = pos_where_quality_was_provided.aggregate(Sum("quality_rating", default=0))
            total_sum_quality_rating = temp['quality_rating__sum']
            average_quality_rating_sum = (total_sum_quality_rating / pos_where_quality_was_provided.count())
            vendor.quality_rating_avg = average_quality_rating_sum    
            
        # Calculate and update fulfillment rate
        if instance.status is not previous_status:
            print("Inside calc of Fulfillment Rate")
            if completed_pos.count() == 0 or all_pos.count() == 0:
                vendor.on_time_delivery_rate = 0
                vendor.quality_rating_avg = 0
                vendor.save()
                return
            vendor.fulfillment_rate = completed_pos.count() / all_pos.count()
            
        vendor.save()
