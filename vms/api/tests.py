from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Vendor, PurchaseOrder
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone

class VendorAPITest(TestCase):
    def setUp(self):
        """
        Setting up APIClient and fake data for testing
        """
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(
            name="Vendor 1",
            contact_details="Contact 1",
            address="Address 1",
            city="City 1"
        )
        self.vendor2 = Vendor.objects.create(
            name="Vendor 2",
            contact_details="Contact 2",
            address="Address 2",
            city="City 2"
        )
        # Generating authentication tokens
        self.user = User.objects.create_user(username='testuser', password='password')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)

    def test_list_all_vendors_without_auth(self):
        """
        Check that fetching of all_vendors is not possible without providing authorization
        details
        """
        url = reverse('all vendors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_vendors(self):
        """
        Check that all vendors are fethced properly. Assume there are only
        2 vendors in this test case
        """
        url = reverse('all vendors')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_vendor(self):
        """
        Test creation of a new vendor
        """
        url = reverse('all vendors')
        data = {
            "name": "New Vendor",
            "contact_details": "New Contact",
            "address": "New Address",
            "city": "New City"
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vendor_details(self):
        """
        Test fetching the data of a vendor using its vendor_id
        """
        url = reverse('vendor', kwargs={'vendor_id': self.vendor1.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor 1')

    def test_update_vendor_details(self):
        """
        Test information update of vendor using vendor_id
        """
        url = reverse('vendor', kwargs={'vendor_id': self.vendor1.id})
        data = {
            "name": "Updated Vendor Name"
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Vendor Name')

    def test_delete_vendor(self):
        """
            Test deletion of a vendor using vendor_id
        """
        url = reverse('vendor', kwargs={'vendor_id': self.vendor1.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        """
        Setting up APIClient and fake data for testing
        """
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            city="Test City"
        )
        self.vendor2 = Vendor.objects.create(
            name="Test Vendor2",
            contact_details="Test Contact",
            address="Test Address",
            city="Test City"
        )
        self.po = PurchaseOrder.objects.create(
            vendor=self.vendor,
            delivery_date=timezone.now(),
            items={"item": "Test Item"},
            quantity=1,
        )

        self.po2 = PurchaseOrder.objects.create(
            vendor=self.vendor,
            delivery_date=timezone.now(),
            items={"item": "Test Item"},
            quantity=1,
        )
        # Generating authentication tokens
        self.user = User.objects.create_user(username='testuser', password='password')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)

        
    def test_list_all_vendors_without_auth(self):
        """
        Check that fetching of all purchase orders is not possible without providing authorization
        details
        """
        url = reverse('all vendors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_purchase_orders(self):
        """
        Check that all purchase orders are fethced properly. Assume there are only
        2 purchase orders in this test case
        """
        url = reverse('all orders')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_all_purchase_orders_with_query_params(self):
        """
        Check that all purchase orders are fethced properly of a 
        particular vendor by passing vendor_id as query.
        """
        url = reverse('all orders')
        response = self.client.get(url, {'vendor_id' : self.vendor.id} , HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.vendor.orders.count())

    def test_create_purchase_order(self):
        """
        Test creation of a new Purchase vendor
        """
        url = reverse('all orders')
        data = {
            "vendor": self.vendor.id,
            "delivery_date": "2024-05-10T12:00:00Z",
            "items": {"item": "Test Item"},
            "quantity": 1
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_purchase_order_details(self):
        """
        Test fetching of a purchase order using po_id
        """
        url = reverse('purchase order', kwargs={'po_id': self.po.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vendor'], self.vendor.name)

    def test_update_purchase_order_details(self):
        """
        Test updation of a purchase order using po_id
        """
        url = reverse('purchase order', kwargs={'po_id': self.po.id})
        data = {
            "delivery_date": "2024-05-10T12:00:00Z"
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        """
        Test deletion of a purchae order using po_id
        """
        url = reverse('purchase order', kwargs={'po_id': self.po.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase_order_acknowledge(self):
        """
        Test if purchase order is being properly acknowledged or not
        """
        url = reverse('order acknowledge', kwargs={'po_id' : self.po.id})
        response = self.client.post(url, HTTP_AUTHORIZATION = f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.po.refresh_from_db()

        self.assertLessEqual(self.po.acknowledgement_date , timezone.now())