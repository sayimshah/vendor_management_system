from rest_framework import serializers
from ..models import PurchaseOrder, Vendor

class VendorSerializer(serializers.ModelSerializer):
    # Set default values for read-only fields
    vendor_code = serializers.ReadOnlyField(default=0)
    fulfillment_rate = serializers.ReadOnlyField(default=0)
    average_response_time = serializers.ReadOnlyField(default=0)
    quality_rating_avg = serializers.ReadOnlyField(default=0)
    on_time_delivery_rate = serializers.ReadOnlyField(default=0)

    class Meta:
        model = Vendor
        fields = '__all__'

    def create(self, validated_data):
        # Set the read-only fields to 0 when creating a new vendor
        validated_data['fulfillment_rate'] = 0
        validated_data['average_response_time'] = 0
        validated_data['quality_rating_avg'] = 0
        validated_data['on_time_delivery_rate'] = 0
        
        return super().create(validated_data)


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'items', 'quantity']

class PurchaseListOrderSerializer(serializers.ModelSerializer):
    # Add vendor name as a read-only field
    vendor_name =  serializers.ReadOnlyField(source='vendor.name')
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor_name', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']


class UpdatePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['quantity', "quality_rating"]  # Include only the fields that can be updated
