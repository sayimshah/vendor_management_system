from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Vendor, PurchaseOrder

class VendorAPITest(APITestCase):
    def setUp(self):
        self.vendor1 = Vendor.objects.create(name="Vendor 1", contact_details="Contact 1", address="Address 1", vendor_code="V001")
        self.vendor2 = Vendor.objects.create(name="Vendor 2", contact_details="Contact 2", address="Address 2", vendor_code="V002")

    def test_get_vendor_list(self):
        url = reverse('vendor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_vendor(self):
        url = reverse('vendor-list')
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)

    # Add more test methods for other CRUD operations on Vendor model

class PurchaseOrderAPITest(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Vendor", contact_details="Contact", address="Address", vendor_code="V001")
        self.purchase_order = PurchaseOrder.objects.create(po_number="PO001", vendor=self.vendor, order_date="2024-05-10", delivery_date="2024-05-17", items=[], quantity=10, status="pending")

    def test_get_purchase_order_detail(self):
        url = reverse('purchase_order_details', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO001')

    def test_create_purchase_order(self):
        url = reverse('purchase_order_create')
        data = {
            'po_number': 'PO002',
            'vendor': self.vendor.id,
            'order_date': '2024-05-11',
            'delivery_date': '2024-05-18',
            'items': [],
            'quantity': 20,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

