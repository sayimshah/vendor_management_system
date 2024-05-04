from django.urls import path, include
from rest_framework import routers
from .views import PurchaseOrderAcknowledgement, PurchaseOrderCreate, PurchaseOrderDetail, VendorList , VendorDetail, VendorPerformance



router = routers.DefaultRouter()


urlpatterns=[
    
    # Include router-generated URLs
    path('', include(router.urls)),
    
    # Vendor URLs
    path('vendors/', VendorList.as_view(), name='vendor-list'),  # List and create vendors
    path('vendors/<int:pk>/', VendorDetail.as_view(), name='vendor-detail'),  # Retrieve, update, and delete vendors by ID
    path('vendors/<int:vendor_id>/performance', VendorPerformance.as_view(), name='vendor-performance'),  # Retrieve vendor performance metrics
    
    # Purchase Order URLs
    path('purchase_orders/', PurchaseOrderCreate.as_view(), name='purchase_order_create'),  # Create a purchase order
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetail.as_view(), name='purchase_order_details'),  # Retrieve, update, and delete a purchase order by ID
    path('purchase_orders/<int:po_id>/acknowledge', PurchaseOrderAcknowledgement.as_view(), name='purchase_order_details'),  # Acknowledge a purchase order
]