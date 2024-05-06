from django.test import TestCase
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorTestCase(TestCase):

    def setUp(self):
        self.vendor1 = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            city="Test City"
        )

        self.vendor2 = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            city="Test City"
        )

        self.po = PurchaseOrder.objects.create(
            vendor=self.vendor1,
            delivery_date=timezone.now() - timezone.timedelta(seconds=10),
            items={"item": "Test Item"},
            quantity=1,
        )

        self.po2 = PurchaseOrder.objects.create(
            vendor=self.vendor2,
            delivery_date=timezone.now() - timezone.timedelta(seconds=10),
            items={"item": "Test Item"},
            quantity=1,
            status='completed'
        )
        

    def test_vendor_creation(self):
        """Check vendor_code length and other default values if not provided must be set to 0"""
        self.assertLessEqual(len(self.vendor1.vendor_code), 18)
        self.assertEqual(self.vendor1.on_time_delivery_rate,0)
        self.assertEqual(self.vendor1.average_response_time,0)
        self.assertEqual(self.vendor1.quality_rating_avg,0)
        self.assertEqual(self.vendor1.fulfillment_rate,0)

    def test_unique_vendor_code(self):
        """Check that if two vendors are created for same city and same time, 
           vendor_code are different for them
        """
        self.assertNotEquals(self.vendor1.vendor_code, self.vendor2.vendor_code)

    def test_total_purchase_orders(self):
        total_pos = self.vendor1.orders.count()
        self.assertEquals(total_pos, 1)

    def test_performance_metrics_handler(self):
        """Check proper working of realtime performance metrics of 
            Vendors based on changes in Purchase orders
        """
        self.po.status = "completed"
        self.po.quality_rating = 4.0
        self.po.issue_date = timezone.now()
        self.po.acknowledgement_date = timezone.now() + timezone.timedelta(seconds=10)
        self.po.save()

        self.vendor1.refresh_from_db()


        # Assert statements to verify the performance metrics
        self.assertEqual(self.vendor1.quality_rating_avg, 4)
        self.assertEqual(self.vendor1.fulfillment_rate, 1)
        self.assertGreaterEqual(self.vendor1.average_response_time, 10)
        self.assertGreaterEqual(self.vendor1.on_time_delivery_rate, 0)

    def test_total_completed_pos(self):
        completed_pos = self.vendor2.orders.filter(status="completed").count()
        self.assertEqual(completed_pos,1)

class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            city="Test City"
        )

        self.po1 = PurchaseOrder.objects.create(
            vendor=self.vendor,
            delivery_date=timezone.now() - timezone.timedelta(seconds=10),
            items={"item": "Test Item"},
            quantity=1,
        )

        self.po2 = PurchaseOrder.objects.create(
            vendor=self.vendor,
            delivery_date=timezone.now() - timezone.timedelta(seconds=10),
            items={"item": "Test Item"},
            quantity=1,
        )

    def test_unique_po_number(self):
        """Check that if two purchase orders are created at same time, 
           po_number are different for them
        """
        self.assertNotEquals(self.po1.po_number, self.po2.po_number)



class HistoricalPerformanceTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            city="Test City",
            on_time_delivery_rate=0.9,
            quality_rating_avg=4.5,
            average_response_time=24,
            fulfillment_rate=0.95
        )

    def test_historical_performance_creation(self):
        historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor
        )
        self.assertEqual(historical_performance.on_time_delivery_rate, 0.9)
        self.assertEqual(historical_performance.quality_rating_avg, 4.5)
        self.assertEqual(historical_performance.average_response_time, 24)
        self.assertEqual(historical_performance.fullfilment_rate, 0.95)
