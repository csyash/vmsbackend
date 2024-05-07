from rest_framework.decorators import  permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from base.models import PurchaseOrder, Vendor, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone


# Create your views here.


# Requires an access token 'Bearer <token>' to access this view
@permission_classes([IsAuthenticated])
class ListAllVendors(APIView):

    # view to list all the vendor and their information
    def get(self, request):
        all_vendors = Vendor.objects.all()
        serializer = VendorSerializer(all_vendors, many=True)
        return Response(serializer.data)
    
    # view for creating a new vendor
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"message" : "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    

# Requires an access token 'Bearer <token>' to access this view
@permission_classes([IsAuthenticated])
class ListVendorDetails(APIView):

    # view to get the information about a vendor through vendor_id
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
                
     # view to update the information of vendor through vendor_id               
    def put(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    
    # view to delete a vendor through vendor_id
    def delete(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        vendor.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Requires an access token 'Bearer <token>' to access this view
@permission_classes([IsAuthenticated])
class ListAllPuchaseOrders(APIView):

    # view to list all the purchase orders and their information
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            vendor = get_object_or_404(Vendor, pk=vendor_id)
            all_po = vendor.orders.all()
        else:
            all_po = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(all_po, many=True)
        return Response(serializer.data)
    
    # view for creating a new purchase order
    def post(self, request):
        vendor_id : int = request.data.pop('vendor')
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        try:
            new_po = PurchaseOrder.objects.create(vendor=vendor, **request.data)
            new_po.save()
            serializer = PurchaseOrderSerializer(new_po)
            return Response(serializer.data)
        except:
            return Response({"message":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    

# Requires an access token 'Bearer <token>' to access this view
@permission_classes([IsAuthenticated])
class ListPurchaseOrder(APIView):

    # view to get the information about a purchase order through po_id
    def get(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # view to delete a purchase order through po_id
    def delete(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(po)
        po.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # view to update the information of purchase order through po_id
    def put(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        if request.data.get('vendor') is not None:
            vendor_id_received = request.data.pop('vendor')

            if po.vendor.id != vendor_id_received:
                vendor_received = get_object_or_404(Vendor, pk=vendor_id_received)
                po.vendor = vendor_received

        serializer = PurchaseOrderSerializer(po, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    

# Requires an access token 'Bearer <token>' to access this view
@permission_classes([IsAuthenticated])
class ListVendorPerformance(APIView):
    # view to get the information about vendor along with its average performance metrics through vendor_id
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vhp = HistoricalPerformance.objects.filter(vendor=vendor).all()
        serializer = HistoricalPerformanceSerializer(vhp, many=True)
        return Response(serializer.data)
    

# Requires an access token 'Bearer <token>' to access this view
@permission_classes([IsAuthenticated])
class AcknowledgePurchaseOrder(APIView):

    # view for vendor to acknowledge its purchase order through po_id and vendor_id. This triggers recalculation of average 
    # response time of vendor
    def post(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        vendor_id_received = request.data.get('vendor_id')
        if po.vendor.id == vendor_id_received:        
            po.acknowledgement_date = timezone.now()
            po.save()

            return Response({"message":"Acknowledge Success"}, status=status.HTTP_200_OK)
        
        return Response({"message":"Unauthorised"}, status=status.HTTP_403_FORBIDDEN)
    


