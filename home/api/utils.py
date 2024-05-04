from random import randint, choice
import string
from ..models import Vendor, PurchaseOrder

def generate_unique_vendor_code():
    """
    Generates a unique vendor code.

    Returns:
        str: A unique vendor code.
    """
    # Generate a random vendor code
    vendor_code = ''.join(str(randint(0, 9)) for _ in range(6))

    # Check if the generated code already exists in the database
    while Vendor.objects.filter(vendor_code=vendor_code).exists():
        vendor_code = ''.join(str(randint(0, 9)) for _ in range(6))

    return vendor_code


def generate_unique_po_number(length=10):
    """
    Generates a unique purchase order number.

    Args:
        length (int): The length of the generated unique code.

    Returns:
        str: A unique purchase order number.
    """
    characters = string.ascii_letters + string.digits
    unique_code = ''.join(choice(characters) for _ in range(length))
    while PurchaseOrder.objects.filter(po_number=unique_code).exists():
        unique_code = ''.join(choice(characters) for _ in range(length))
    return unique_code
