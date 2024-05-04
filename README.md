# vendor_management_system
git clone (https://github.com/sayimshah/vendor_management_system.git)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
API Endpoints
Vendor List Endpoint:
Method: GET/POST
URL: /api/vendors/
Description: Retrieves a list of all vendors or creates a new vendor.
Vendor Detail Endpoint:
Method: GET/PUT/DELETE
URL: /api/vendors/<int:pk>/
Description: Retrieves, updates, or deletes a specific vendor.
Purchase Order Create Endpoint:
Method: GET/POST
URL: /api/purchase_orders/
Description: Creates a new purchase order or retrieves a list of purchase orders.
Purchase Order Detail Endpoint:
Method: GET/PUT/DELETE
URL: /api/purchase_orders/<int:po_id>/
Description: Retrieves, updates, or deletes a specific purchase order.
Purchase Order Acknowledgement Endpoint:
Method: PUT
URL: /api/purchase_orders/<int:po_id>/acknowledge
Description: Acknowledges a purchase order by updating its status.
Vendor Performance Endpoint:
Method: GET
URL: /api/vendors/<int:vendor_id>/performance
Description: Retrieves performance metrics for a specific vendor


cd purchase_order_management
python manage.py test
