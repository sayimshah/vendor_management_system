from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def clean(self):
        if self.fulfillment_rate > 100:
            raise ValidationError("Fulfillment rate cannot be greater than 100%.")

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    quality_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.status == PurchaseOrder.COMPLETED and not self.quality_rating:
            raise ValidationError("Quality rating is required for completed orders.")

    def __str__(self):
        return self.po_number
    
class VendorPerformanceRecord(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def clean(self):
        if self.fulfillment_rate > 100:
            raise ValidationError("Fulfillment rate cannot be greater than 100%.")

    def __str__(self):
        return f"Performance Record for {self.vendor.name} on {self.date}"
