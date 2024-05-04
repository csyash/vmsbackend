from django.contrib import admin

from .models import Vendor, PurchaseOrder, HistoricalPerformance
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    readonly_fields = ('vendor_code',)

class PurchaseOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('po_number',)

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    readonly_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time' , 'fullfilment_rate')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)