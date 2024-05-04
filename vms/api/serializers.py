from base.models import PurchaseOrder, Vendor, HistoricalPerformance
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        

class PurchaseOrderSerializer(ModelSerializer):
    vendor = SerializerMethodField()
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    def get_vendor(self, obj):
        return obj.vendor.name
    
class HistoricalPerformanceSerializer(ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
        depth=1