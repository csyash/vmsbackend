from base.models import PurchaseOrder, Vendor, HistoricalPerformance
from rest_framework.serializers import ModelSerializer, SerializerMethodField

# serializer for Vendor
class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        

# serializer for Purchase Order
class PurchaseOrderSerializer(ModelSerializer):
    # Changing the 'vendor' of serializer from 'vendor_id' to 'vendor name'
    vendor = SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    # getting the name of vendor of the purchase order
    def get_vendor(self, obj):
        return obj.vendor.name
    
# Historical Performance Serializer
class HistoricalPerformanceSerializer(ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
        depth=1