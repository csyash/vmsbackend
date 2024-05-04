from django.contrib import admin

from .models import Vendor, PurchaseOrder, HistoricalPerformance
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    # Making the vendor_code read_only because we create it manually by overriding save() method in Vendor model
    readonly_fields = ('vendor_code',)

class PurchaseOrderAdmin(admin.ModelAdmin):
    # Making the po_number read_only because we create it manually by overriding save() method in PurchaseOrder model
    readonly_fields = ('po_number',)

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    # Making every field except vendor read_only because every field is a snapshot of Vendor's performance metrics.
    # We update the snapshot information manually by overriding save() method in HistoricalPerformance model.
    readonly_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time' , 'fullfilment_rate')


# Registration of Models to the django admin panel
admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)