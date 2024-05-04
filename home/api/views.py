from django.utils import timezone
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import PurchaseOrder, Vendor
from .signals import update_vendor_metrics
from .serializers import PurchaseListOrderSerializer, PurchaseOrderSerializer, UpdatePurchaseOrderSerializer, VendorSerializer
from .utils import generate_unique_po_number, generate_unique_vendor_code
from django.db.models import Avg, Count

class VendorList(APIView):
    """
    API endpoint to list all vendors or create a new vendor.
    """
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a unique vendor code
            vendor_code = generate_unique_vendor_code()
            # Save the serializer instance
            serializer.save(vendor_code=vendor_code)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetail(APIView):
    """
    API endpoint to retrieve, update, or delete a specific vendor.
    """
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderCreate(APIView):
    """
    API endpoint to create a new purchase order or list purchase orders.
    """
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a unique PO number (you can implement your own logic here)
            po_number = generate_unique_po_number()
            
            # Set the order date as today's date
            # Assuming today's date as the order date
            order_date = timezone.now().date()

            # Assuming delivery date is 7 days from the order date
            delivery_date = order_date + timezone.timedelta(days=7)
            
            # Set the generated values in the serializer
            serializer.save(po_number=po_number, order_date=order_date, delivery_date=delivery_date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseListOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    
class PurchaseOrderDetail(APIView):
    """
    API endpoint to retrieve, update, or delete a specific purchase order.
    """
    def get(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            serializer = PurchaseListOrderSerializer(purchase_order)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            serializer = UpdatePurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
            if 'quality_rating' in request.data and purchase_order.status == 'pending':
                return Response({"message":"order is Pending, Can`t provide rating"}
                                ,status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()


                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found."}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found."}
                            , status=status.HTTP_404_NOT_FOUND)

class PurchaseOrderAcknowledgement(APIView):
    """
    API endpoint to acknowledge a purchase order.
    """
    def put(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            new_status = request.data.get('status')
            if new_status not in [status[0] for status in PurchaseOrder.STATUS_CHOICES]:
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            old_status = purchase_order.status
            purchase_order.status = new_status
            # Update acknowledgment date to today's date if the new status is accepted or completed
            if new_status in [PurchaseOrder.ACCEPTED, PurchaseOrder.COMPLETED]:
                purchase_order.acknowledgment_date = timezone.now().date()
            
            purchase_order.save()

            # If status has changed and new status is ACCEPTED or COMPLETED, trigger signal
            if old_status != new_status and new_status in [PurchaseOrder.ACCEPTED, PurchaseOrder.COMPLETED]:
                update_vendor_metrics(purchase_order.vendor)

            return Response({"message": "Purchase order status updated successfully"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found."}, status=status.HTTP_404_NOT_FOUND)
        
class VendorPerformance(APIView):
    """
    API endpoint to retrieve performance metrics for a specific vendor.
    """
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)

            performance_data = {
                'vendor_ID' : vendor.pk,
                'vendor_name' : vendor.name,
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate
            }

            return Response(performance_data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
