from ..models import PurchaseOrder , VendorPerformanceRecord
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.utils import timezone




@receiver(post_save, sender=PurchaseOrder)
def update_vendor_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_ratings = completed_pos.exclude(quality_rating__isnull=True).count()
        total_quality_rating = completed_pos.exclude(quality_rating__isnull=True).aggregate(total_rating=Avg('quality_rating'))['total_rating'] or 0

        # Calculate the updated quality rating average
        if total_ratings > 0:
            new_quality_rating_avg = total_quality_rating / total_ratings
            new_quality_rating_avg = round(new_quality_rating_avg, 2)  # Round to two decimal places
        else:
            new_quality_rating_avg = 0

        # Update the vendor's quality rating average
        vendor.quality_rating_avg = new_quality_rating_avg
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if instance.status == PurchaseOrder.ACCEPTED or instance.status == PurchaseOrder.COMPLETED:
        vendor = instance.vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status__in=[PurchaseOrder.ACCEPTED, PurchaseOrder.COMPLETED])
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / 3600 for po in purchase_orders if po.acknowledgment_date]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0

        fulfilment_rate = purchase_orders.filter(status=PurchaseOrder.COMPLETED).count() / purchase_orders.count() * 100 if purchase_orders.count() > 0 else 0
        
        # Calculate On-Time Delivery Rate
        if instance.status == PurchaseOrder.COMPLETED:
            completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status=PurchaseOrder.COMPLETED)
            on_time_orders = completed_orders.filter(delivery_date__lte=instance.delivery_date)
            on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0
            vendor.on_time_delivery_rate = on_time_delivery_rate

        vendor.average_response_time = round(average_response_time, 2)
        vendor.fulfillment_rate = fulfilment_rate
        vendor.save()
        # Save data in VendorPerformanceRecord
        performance_record = VendorPerformanceRecord(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=fulfilment_rate
        )
        performance_record.save()